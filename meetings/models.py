from django.db import models
from accounts.models import User
import uuid
from django.core.exceptions import ValidationError
from integrations import create_zoom_meeting, update_zoom_meeting

class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)  
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class ZoomMeeting(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    timezone = models.CharField(max_length=64)
    def __str__(self):
        return f"Zoom meeting on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

def create_zoom_meeting_for_meeting(meeting_instance):
    try:
        start_time_dt = meeting_instance.start_time
        end_time_dt = meeting_instance.end_time
        start_time = start_time_dt.isoformat()
        duration = int((end_time_dt - start_time_dt).total_seconds() / 60)
        
        if duration <= 0:
            raise ValidationError("Meeting duration must be positive")
                
        try:
            zoom_data = create_zoom_meeting(
                topic=meeting_instance.description,
                agenda='A meeting created by eventio.',
                start_time=start_time,
                duration=duration,
                time_zone='Europe/London',
                max_participants=meeting_instance.get_number_invites,
            )
        except Exception as e:
            print(f"Zoom API Error: {str(e)}")
            raise ValidationError(f"Failed to create Zoom meeting: {str(e)}")
        
        if not zoom_data or 'id' not in zoom_data or 'join_url' not in zoom_data:
            raise ValidationError("Invalid response from Zoom API")
            
        zoom_meeting = ZoomMeeting.objects.create(
            id=zoom_data['id'],
            url=zoom_data['join_url'],
            start_time=start_time_dt,
            end_time=end_time_dt,
            timezone='Europe/London',
        )
        
        return zoom_meeting
        
    except ValidationError:
        raise
    except Exception as e:
        print(f"Unexpected error creating Zoom meeting: {str(e)}")
        raise ValidationError("An unexpected error occurred while creating the Zoom meeting")

def update_zoom_meeting_for_meeting(meeting_instance):
    """
    Updates an existing Zoom meeting when a Meeting model is modified.
    """
    try:
        if not meeting_instance.zoom_meeting:
            raise ValidationError("No Zoom meeting associated with this meeting")
            
        start_time_dt = meeting_instance.start_time
        end_time_dt = meeting_instance.end_time
        start_time = start_time_dt.isoformat()
        duration = int((end_time_dt - start_time_dt).total_seconds() / 60)
        
        if duration <= 0:
            raise ValidationError("Meeting duration must be positive")
        
        print(f"Updating Zoom meeting {meeting_instance.zoom_meeting.id} scheduled to start at {start_time} for {duration} minutes")
        
        try:
            zoom_data = update_zoom_meeting(
                meeting_id=str(meeting_instance.zoom_meeting.id),
                topic=meeting_instance.description,
                agenda='A meeting created by eventio.',
                start_time=start_time,
                duration=duration,
                time_zone='Europe/London',
                max_participants=meeting_instance.get_number_invites,
            )
        except Exception as e:
            print(f"Zoom API Error: {str(e)}")
            raise ValidationError(f"Failed to update Zoom meeting: {str(e)}")
        
        if not zoom_data or 'id' not in zoom_data or 'join_url' not in zoom_data:
            raise ValidationError("Invalid response from Zoom API")
            
        zoom_meeting = meeting_instance.zoom_meeting
        zoom_meeting.url = zoom_data['join_url']
        zoom_meeting.start_time = start_time_dt
        zoom_meeting.end_time = end_time_dt
        zoom_meeting.save()
        
        return zoom_meeting
        
    except ValidationError:
        raise
    except Exception as e:
        print(f"Unexpected error updating Zoom meeting: {str(e)}")
        raise ValidationError("An unexpected error occurred while updating the Zoom meeting")

class Meeting(models.Model):
    meeting_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=256)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organised_meetings')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    zoom_meeting = models.OneToOneField(ZoomMeeting, null=True, blank=True, on_delete=models.SET_NULL)
    is_virtual = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        if not self.place and not self.zoom_meeting and not self.is_virtual:
            raise ValidationError("A meeting must have either a place or be virtual (with a Zoom meeting).")

    def save(self, *args, **kwargs):
        self.clean()  # Perform validation before saving
        
        is_new = self.pk is None
        
        needs_zoom_update = False
        if not is_new and self.is_virtual and self.zoom_meeting:
            original = Meeting.objects.get(pk=self.pk)
            if (original.description != self.description or
                original.start_time != self.start_time or
                original.end_time != self.end_time):
                needs_zoom_update = True
        
        super().save(*args, **kwargs)

        if self.is_virtual:
            if is_new or self.zoom_meeting is None:
                try:
                    new_zoom = create_zoom_meeting_for_meeting(self)
                    self.zoom_meeting = new_zoom
                    super().save(update_fields=['zoom_meeting'])
                except ValidationError as e:
                    print(f"Failed to create Zoom meeting: {str(e)}")
            elif needs_zoom_update:
                try:
                    update_zoom_meeting_for_meeting(self)
                except ValidationError as e:
                    print(f"Failed to update Zoom meeting: {str(e)}")

    def get_confirmed_attendees(self, exclude_user=None, include_organiser=False):
        attendees = User.objects.filter(
            invitations__meeting=self,
            invitations__status=True
        )
        
        if include_organiser:
            organiser_qs = User.objects.filter(id=self.organiser.id)
            attendees = (attendees | organiser_qs).distinct()
        
        if exclude_user:
            attendees = attendees.exclude(id=exclude_user.id)
            
        return attendees
    
    @property
    def get_number_invites(self):
        """
        Returns the number of invitations for this meeting.
        """
        return Invitation.objects.filter(meeting=self).count()
    
class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='invitations')
    time_created = models.DateTimeField(auto_now_add=True)
    time_amended = models.DateTimeField(auto_now=True)
    status = models.BooleanField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('user', 'meeting')

    def __str__(self):
        return f"Invitation for {self.user.username} to meet {self.meeting}"
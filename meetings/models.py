from django.db import models
from accounts.models import User
import uuid

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
    meeting_password = models.CharField(max_length=128)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    timezone = models.CharField(max_length=64)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organised_zoom_meetings')

    def __str__(self):
        return f"Zoom meeting on {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Meeting(models.Model):
    meeting_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=256)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organised_meetings')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.description} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

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
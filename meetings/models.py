from django.db import models
from accounts.models import User
import uuid
from django.core.exceptions import ValidationError

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
    zoom_meeting = models.OneToOneField(ZoomMeeting, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.description} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        # Ensure that either a place or a Zoom meeting is provided
        if not self.place and not self.zoom_meeting:
            raise ValidationError("A meeting must have either a place or a Zoom meeting.")

    def save(self, *args, **kwargs):
        self.clean()  # Perform validation
        super().save(*args, **kwargs)  # Call the original save method
    
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
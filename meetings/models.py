from django.db import models
from accounts.models import User

class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=256) # TODO: Robbie to implement a Location Integeration
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=256)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organised_meetings')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.description} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='invitations')
    time_created = models.DateTimeField(auto_now_add=True)
    time_amended = models.DateTimeField(auto_now=True)
    status = models.NullBooleanField(default=None)

    class Meta:
        unique_together = ('user', 'meeting')

    def __str__(self):
        return f"Invitation for {self.user.username} to meet {self.meeting}"


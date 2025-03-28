import uuid
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now, timedelta
from meetings.models import Meeting, Place, Invitation
from django.http import Http404

User = get_user_model()

class MeetingsTestCase(TestCase):
    def setUp(self):
        """Set up test users, places, and meetings"""
        self.client = Client()

        # Create test users
        self.user1 = User.objects.create_user(email="user1@example.com", password="testpass", first_name="First", last_name="Last")
        self.user2 = User.objects.create_user(email="user2@example.com", password="testpass", first_name="First", last_name="Last")

        # Create a place
        self.place = Place.objects.create(name="Test Place", address="123 Main St", capacity=50)

        # Create a meeting
        self.meeting = Meeting.objects.create(
            meeting_id=uuid.uuid4(),
            description="Test Meeting",
            start_time=now() + timedelta(days=1),
            end_time=now() + timedelta(days=1, hours=1),
            organiser=self.user1,
            place=self.place
        )

        # Create an invitation
        self.invitation = Invitation.objects.create(user=self.user2, meeting=self.meeting, status=True)

    def test_meeting_creation(self):
        """Test that a meeting is created successfully"""
        self.assertEqual(Meeting.objects.count(), 1)
        self.assertEqual(self.meeting.organiser, self.user1)

    def test_invitation_creation(self):
        """Test that an invitation is created successfully"""
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertTrue(self.invitation.status)

    def test_get_confirmed_attendees(self):
        """Test the get_confirmed_attendees method"""
        attendees = self.meeting.get_confirmed_attendees()
        self.assertIn(self.user2, attendees)
        self.assertNotIn(self.user1, attendees)  # Organiser not included by default

    def test_meeting_view_requires_login(self):
        """Test that a user must be logged in to view a meeting"""
        response = self.client.get(reverse("meetings:view_meeting", args=[str(self.meeting.pk)]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=' + reverse("meetings:view_meeting", args=[str(self.meeting.pk)]))

    def test_api_meetings(self):
        """Test fetching meetings through API"""
        response = self.client.get(reverse("meetings:get_meetings"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

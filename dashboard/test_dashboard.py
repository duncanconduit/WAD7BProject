from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from meetings.models import Meeting, Invitation, Place
from django.utils import timezone

User = get_user_model()

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user for the organiser
        self.organiser = User.objects.create_user(email='test@example.com', password='testpassword')

        # Create a test place for the meeting
        self.place = Place.objects.create(name="Test Place", address="123 Test St", capacity=10)

        # Create a Meeting with the correct fields
        self.meeting = Meeting.objects.create(
            description="Test Meeting",  # description instead of title
            start_time=timezone.now(),   # start_time is required
            end_time=timezone.now() + timezone.timedelta(hours=1),  # set the end time to 1 hour later
            organiser=self.organiser,   # the User as organiser
            place=self.place            # Place as the meeting location
        )

    def test_calendar_view(self):
        # Test your calendar view functionality here
        response = self.client.get('/calendar/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Meeting")

    def test_create_meeting_view(self):
        # Test creating a meeting
        response = self.client.post('/create_meeting/', {
            'description': 'New Meeting',
            'start_time': timezone.now(),
            'end_time': timezone.now() + timezone.timedelta(hours=2),
            'organiser': self.organiser.id,
            'place': self.place.id,
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirect after creation
        self.assertTrue(Meeting.objects.filter(description='New Meeting').exists())

    def test_dashboard_view(self):
        # Test dashboard view functionality
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Meeting")

    def test_index_view(self):
        # Test index view functionality
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Meeting")

    def test_meetings_view(self):
        # Test meetings view functionality
        response = self.client.get('/meetings/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Meeting")

    def test_notifications_view(self):
        # Test notifications view functionality
        response = self.client.get('/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Meeting")
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from meetings.models import Meeting, Invitation,Place
from accounts.models import User

class DashboardViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.place = Place.objects.create(
            name="Conference Room",
            address="123 Office St",
            capacity=10
        )
        self.meeting = Meeting.objects.create(
            organiser=self.user,
            description="Weekly Standup",
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2),
            place=self.place,
            is_virtual=False
        )
        self.invitation = Invitation.objects.create(
            user=self.user,
            meeting=self.meeting,
            status=None
        )

    def test_index_view_authenticated_redirect(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('dashboard:index'))
        self.assertRedirects(response, reverse('dashboard:dashboard'))

    def test_index_view_unauthenticated(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_dashboard_view_authenticated(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')


    def test_notifications_view_authenticated(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(reverse('dashboard:notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/notifications.html')

    def test_dashboard_invitation_status_update(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(reverse('dashboard:dashboard'), {
            'invitation_id': self.invitation.id,
            'worktype': 'True'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Status updated successfully.'})
        self.invitation.refresh_from_db()
        self.assertTrue(self.invitation.status)

from django.urls import path
from meetings import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('',  RedirectView.as_view(url='/accounts/meetings/', permanent=True), name='meetings'),
    path('view/<int:meeting_id>/', views.meeting_view, name='meeting_view'),
    path('create/', views.meeting_create, name='create_meeting'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/meetings/', views.get_meetings, name='get_meetings'),
]

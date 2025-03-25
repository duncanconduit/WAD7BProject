from django.urls import path
from meetings import views
from django.views.generic.base import RedirectView

app_name = 'meetings' 
urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/meetings/', permanent=True), name='meetings'),
    path('meetings/meeting/<uuid:meeting_id>/edit/', views.edit_meeting, name='edit_meeting'),
    path('meetings/meeting/<uuid:meeting_id>/', views.meeting_view, name='view_meeting'),  
    path('create/', views.create_meeting, name='create_meeting'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/meetings/', views.get_meetings, name='get_meetings'),
]

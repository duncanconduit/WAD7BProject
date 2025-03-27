from django.urls import path
from meetings import views
from django.views.generic.base import RedirectView

app_name = 'meetings'

app_name = 'meetings' 
urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/meetings/', permanent=True), name='meetings'),
    path('<uuid:meeting_id>/', views.view_meeting, name='view_meeting'),
    path('<uuid:meeting_id>/edit/', views.edit_meeting, name='edit_meeting'),
    path('create/', views.create_meeting, name='create_meeting'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/meetings/', views.get_meetings, name='get_meetings'),
]

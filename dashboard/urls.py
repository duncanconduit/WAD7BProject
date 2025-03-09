from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('meetings/', views.meetings, name='meetings'),
    path('create_meeting', views.create_meeting, name='create_meeting'),
    path('notifications', views.notifications, name='notifications'),
]

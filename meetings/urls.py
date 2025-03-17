from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/meetings/', views.get_meetings, name='get_meetings'),
]

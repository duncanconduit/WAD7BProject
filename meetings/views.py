from django.shortcuts import render
from .models import Meeting
from django.http import JsonResponse
from django.utils.timezone import now
from django.conf import settings

# view to display meetings as events for calendar api
def calendar_view(request):
    today = now().date()
    meetings = Meeting.objects.filter(start_time__gte=today).order_by('start_time')

    events = [
        {
            'title': meeting.description,
            'start': meeting.start_time.isoformat(),
            'end': meeting.end_time.isoformat(),
            'location': meeting.place.name if meeting.place else 'No location',
        }
        for meeting in meetings
    ]

    context = {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    }

    return JsonResponse(events, safe=False)

# optional additional view to fetch all meetings, if needed for other purposes
def get_meetings(request):
    meetings = Meeting.objects.all()
    events = [
        {
            'title': meeting.description,
            'start': meeting.start_time.isoformat(),
            'end': meeting.end_time.isoformat(),
            'location': meeting.place.name if meeting.place else "TBD",
        }
        for meeting in meetings
    ]
    return JsonResponse(events, safe=False)

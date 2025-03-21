from django.shortcuts import render
from meetings.models import Meeting, Invitation
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

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


@login_required
def meeting_view(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    

    if request.user != meeting.organiser and not meeting.invitations.filter(user=request.user).exists():
        raise Http404("Meeting not found")

    return render(request, 'meetings/view.html', {'meeting': meeting})

@login_required
def meeting_create(request):
    render(request, 'meetings/create.html')

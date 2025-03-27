from django.shortcuts import render
from meetings.models import Meeting, Invitation
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from meetings.models import Meeting, Place

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


@login_required
def view_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    

    if request.user != meeting.organiser and not meeting.invitations.filter(user=request.user).exists():
        raise Http404("Meeting not found")

    return render(request, 'meetings/view.html', {'meeting': meeting})

@login_required
def create_meeting(request):
    return render(request, 'meetings/create.html')

@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    if request.user != meeting.organiser:
        raise Http404("You do not have permission to edit this meeting.")
    
    if request.method == 'POST':
        meeting.description = request.POST.get('description')
        meeting.start_time = parse_datetime(request.POST.get('start_time'))
        meeting.end_time = parse_datetime(request.POST.get('end_time'))
        place_id = request.POST.get('place')
        meeting.place = Place.objects.get(pk=place_id) if place_id else None
        meeting.save()

        return redirect('view',meeting_id=meeting.pk)
    else:
        return render(request, 'meetings/edit.html', {'meeting': meeting})

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
from accounts.models import User
import pytz

def get_london_aware_datetime(dt_str):
    dt_naive = parse_datetime(dt_str)
    if dt_naive is None:
        return None 
    london_tz = pytz.timezone('Europe/London')
    dt_aware = london_tz.localize(dt_naive, is_dst=None)
    return dt_aware

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
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "events": events
    }

    return render(request, 'meetings/calendar.html', context)


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
    places = Place.objects.all()

    context = {
        'places': places,
    }

    if request.method == 'POST':
        description = request.POST.get('description')
        start_time = get_london_aware_datetime(request.POST.get('start_time'))
        end_time = get_london_aware_datetime(request.POST.get('end_time'))
        place_id = request.POST.get('place')
        is_virtual = request.POST.get('is_virtual') == 'True'  # Changed to match JS value
        invitees = request.POST.getlist('invitees')
        
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # Validate inputs
        if invitees and not all(User.objects.filter(email=invitee).exists() for invitee in invitees):
            if is_ajax:
                return JsonResponse({'error': 'Invalid invitee(s) selected.'}, status=400)
            else:
                messages.error(request, 'Invalid invitee(s) selected.')
                return render(request, 'meetings/create.html', context)

        if not description or not start_time or not end_time:
            if is_ajax:
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            else:
                messages.error(request, 'All fields are required.')
                return render(request, 'meetings/create.html', context)

        if start_time >= end_time:
            if is_ajax:
                return JsonResponse({'error': 'End time must be after start time.'}, status=400)
            else:
                messages.error(request, 'End time must be after start time.')
                return render(request, 'meetings/create.html', context)
        
        # For in-person meetings, place is required
        if not is_virtual and not place_id:
            if is_ajax:
                return JsonResponse({'error': 'Place is required for in-person meetings.'}, status=400)
            else:
                messages.error(request, 'Place is required for in-person meetings.')
                return render(request, 'meetings/create.html', context)

        # Get place object only for in-person meetings
        place = None
        if not is_virtual and place_id:
            try:
                place = Place.objects.get(pk=place_id)
            except Place.DoesNotExist:
                if is_ajax:
                    return JsonResponse({'error': 'Invalid place selected.'}, status=400)
                else:
                    messages.error(request, 'Invalid place selected.')
                    return render(request, 'meetings/create.html', context)

        # Create the meeting
        meeting = Meeting(
            description=description,
            start_time=start_time,
            end_time=end_time,
            organiser=request.user,
            place=place,
            is_virtual=is_virtual
        )
        meeting.save()

        # Create invitations from email addresses
        for invitee_email in invitees:
            if invitee_email.strip():  # Only if email is not empty
                try:
                    user = User.objects.get(email=invitee_email)
                    Invitation.objects.create(user=user, meeting=meeting)
                except User.DoesNotExist:
                    # Skip invalid emails - they should have been caught earlier
                    pass

        # Return appropriate response based on request type
        if is_ajax:
            return JsonResponse({
                'success': True, 
                'message': 'Meeting created successfully.',
                'redirect': reverse('meetings:view_meeting', args=[meeting.pk])
            })
        else:
            messages.success(request, 'Meeting created successfully!')
            return redirect(reverse('meetings:view_meeting', args=[meeting.pk]))
    
    return render(request, 'meetings/create.html', context)

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
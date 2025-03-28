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
import datetime

def get_london_aware_datetime(dt_str):
    """
    Parse a datetime string to a timezone-aware datetime object in London timezone.
    Handles both ISO format and HTML5 datetime-local format.
    """
    if not dt_str:
        return None
    
    try:
        dt_naive = parse_datetime(dt_str)
        
        if dt_naive is None and 'T' in dt_str:
            dt_naive = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
            
        if dt_naive is None:
            return None
            
        london_tz = pytz.timezone('Europe/London')
        dt_aware = london_tz.localize(dt_naive, is_dst=None)
        return dt_aware
        
    except (ValueError, TypeError):
        return None

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
        "events": events
    }

    return render(request, 'meetings/calendar.html', context)


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
    invitations = Invitation.objects.filter(meeting=meeting)
    

    if request.user != meeting.organiser and not meeting.invitations.filter(user=request.user).exists():
        raise Http404("Meeting not found")
    
    context = {
        'meeting': meeting,
        'invitations': invitations,
    }

    return render(request, 'meetings/view.html', context)

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
    invitations = Invitation.objects.filter(meeting=meeting)
    places = Place.objects.all()
    
    if request.user != meeting.organiser:
        raise Http404("You do not have permission to edit this meeting.")
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        description = request.POST.get('description')
        start_time = get_london_aware_datetime(request.POST.get('start_time'))
        end_time = get_london_aware_datetime(request.POST.get('end_time'))
        is_virtual = request.POST.get('is_virtual') == 'True'
        place_id = request.POST.get('place')
        invitees = request.POST.getlist('invitees')
        remove_invitations = request.POST.get('remove_invitations', '')
        
        if not description or not start_time or not end_time:
            if is_ajax:
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            else:
                messages.error(request, 'All fields are required.')
                return render(request, 'meetings/edit.html', {'meeting': meeting, 'places': places, 'invitations': invitations})

        if start_time >= end_time:
            if is_ajax:
                return JsonResponse({'error': 'End time must be after start time.'}, status=400)
            else:
                messages.error(request, 'End time must be after start time.')
                return render(request, 'meetings/edit.html', {'meeting': meeting, 'places': places, 'invitations': invitations})
        
        if not is_virtual and not place_id:
            if is_ajax:
                return JsonResponse({'error': 'Place is required for in-person meetings.'}, status=400)
            else:
                messages.error(request, 'Place is required for in-person meetings.')
                return render(request, 'meetings/edit.html', {'meeting': meeting, 'places': places, 'invitations': invitations})

        place = None
        if not is_virtual and place_id:
            try:
                place = Place.objects.get(pk=place_id)
            except Place.DoesNotExist:
                if is_ajax:
                    return JsonResponse({'error': 'Invalid place selected.'}, status=400)
                else:
                    messages.error(request, 'Invalid place selected.')
                    return render(request, 'meetings/edit.html', {'meeting': meeting, 'places': places, 'invitations': invitations})
        
        if invitees and any(e for e in invitees if e.strip() and not User.objects.filter(email=e.strip()).exists()):
            if is_ajax:
                return JsonResponse({'error': 'Invalid invitee(s) selected.'}, status=400)
            else:
                messages.error(request, 'Invalid invitee(s) selected.')
                return render(request, 'meetings/edit.html', {'meeting': meeting, 'places': places, 'invitations': invitations})
        
        meeting.description = description
        meeting.start_time = start_time
        meeting.end_time = end_time
        meeting.is_virtual = is_virtual
        meeting.place = place
        meeting.save()
        
        if remove_invitations:
            invitation_ids = [id.strip() for id in remove_invitations.split(',') if id.strip()]
            Invitation.objects.filter(id__in=invitation_ids, meeting=meeting).delete()
        
        for invitee_email in invitees:
            if invitee_email.strip():  # Only if email is not empty
                user = User.objects.filter(email=invitee_email.strip()).first()
                if user and not Invitation.objects.filter(user=user, meeting=meeting).exists():
                    Invitation.objects.create(user=user, meeting=meeting)
        
        if is_ajax:
            return JsonResponse({
                'success': True, 
                'message': 'Meeting updated successfully.',
                'redirect': reverse('meetings:view_meeting', args=[meeting.pk])
            })
        else:
            messages.success(request, 'Meeting updated successfully!')
            return redirect('meetings:view_meeting', meeting_id=meeting.pk)
    
    context = {
        'meeting': meeting,
        'places': places,
        'invitations': invitations,
    }
    
    return render(request, 'meetings/edit.html', context)
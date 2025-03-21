from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from meetings.models import Meeting, Invitation
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    else:
        return render(request, 'dashboard/index.html')

@login_required
def meetings(request):
    return render(request, 'dashboard/meetings.html')

@login_required
def create_meeting(request):
    return render(request, 'dashboard/create_meeting.html')

@login_required
def notifications(request):
    return render(request, 'dashboard/notifications.html')

def calendar_view(request):
    return render(request, 'dashboard/calendar.html')

@login_required
def dashboard(request):
    user = request.user
    now = timezone.now()

    # Handle invitation status updates
    if request.method == "POST" and 'invitation_id' in request.POST:
        invitation_id = request.POST.get('invitation_id')
        worktype = request.POST.get('worktype')
        
        # Validate that worktype is provided
        if worktype is None:
            print("No status provided.")
            return JsonResponse({'success': False, 'message': 'No status provided.'})
        
        # Convert worktype value to a boolean (or None)
        if worktype == "True":
            status_value = True
        elif worktype == "False":
            status_value = False
        elif worktype == "None":
            status_value = None
        else:
            return JsonResponse({'success': False, 'message': 'Unexpected status value.'})
        
        try:
            invitation = Invitation.objects.get(pk=invitation_id)
        except Invitation.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invitation not found.'})
        
        if invitation.user != user:
            return JsonResponse({'success': False, 'message': 'Invitation does not belong to the current user.'})
        
        invitation.status = status_value
        invitation.save()
        return JsonResponse({'success': True, 'message': 'Status updated successfully.'})

    up_next = Meeting.objects.filter(
        start_time__gt=now,
        start_time__lte=now + timedelta(days=1)
    ).filter(
        Q(organiser=user) | Q(invitations__user=user, invitations__status=True)
    ).distinct().prefetch_related('invitations__user')

    organising = Meeting.objects.filter(
        organiser=user
    ).order_by('start_time').prefetch_related('invitations__user')

    attending = Meeting.objects.filter(
        invitations__user=user,
        invitations__status=True
    ).exclude(
        organiser=user
    ).order_by('start_time').prefetch_related('invitations__user')

    a_look_ahead = Meeting.objects.filter(
        start_time__gt=now + timedelta(days=1)
    ).filter(
        Q(organiser=user) | Q(invitations__user=user, invitations__status=True)
    ).distinct().order_by('start_time').prefetch_related('invitations__user')

    invites_section_none = Meeting.objects.filter(
        invitations__user=user,
        invitations__status=None
    ).distinct()

    invites_section_false = Meeting.objects.filter(
        invitations__user=user,
        invitations__status=False
    ).distinct()

    invites_section = invites_section_none.union(invites_section_false).order_by('start_time')

    invites = Invitation.objects.filter(
        user=user
    ).order_by('time_created')

    context = {
        'up_next': up_next,
        'organising': organising,
        'attending': attending,
        'a_look_ahead': a_look_ahead,
        'invites_section': invites_section,
        'invites': invites,
    }
    return render(request, 'dashboard/dashboard.html', context)
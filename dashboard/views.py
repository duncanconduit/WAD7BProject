from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from meetings.models import Meeting

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    else:
        return render(request, 'dashboard/index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def meetings(request):
    meeting_list = list(Meeting.objects.values("latitude", "longitude"))  
    context = {"meetings": meeting_list}
    return render(request, "dashboard/meetings.html", context)

@login_required
def create_meeting(request):
    return render(request, 'dashboard/create_meeting.html')

@login_required
def notifications(request):
    return render(request, 'dashboard/notifications.html')

def calendar_view(request):
    return render(request, 'dashboard/calendar.html')

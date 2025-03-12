from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'dashboard/index.html')
def meetings(request):
    return render(request,'dashboard/meetings.html')
def create_meeting(request):
    return render(request,'dashboard/create_meeting.html')
def notifications(request):
    return render(request,'dashboard/notifications.html')

def calendar_view(request):
    return render(request, 'dashboard/calendar.html')


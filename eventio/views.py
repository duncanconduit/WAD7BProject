from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def contact(request):
    return render(request,'contact.html')

@login_required
def about(request):
    return render(request,'about.html')
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        next_url = request.POST.get('next') or request.GET.get('next')
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({'success': True, 'redirect': next_url or reverse('dashboard:index')})
            else:
                return JsonResponse({'success': False, 'message': 'Sorry, there was an error. Please contact support.'})
        else:
             return JsonResponse({'success': False, 'message': 'Invalid email or password.'})
    else:
        return render(request, 'accounts/login.html')
    
@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse('dashboard:index'))

def profile(request):
    return render(request,'accounts/profile.html')
def register(request):
    return render(request,'accounts/register.html')
def settings(request):
    return render(request,'accounts/settings.html')
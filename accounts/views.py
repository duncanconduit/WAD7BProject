from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from accounts.models import User, Organisation

def login(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect(reverse('dashboard:index'))

@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse('dashboard:index'))

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        updated = False

        new_first_name = request.POST.get('first_name', '').strip()
        new_last_name = request.POST.get('last_name', '').strip()
        new_email = request.POST.get('email', '').strip()

        if new_first_name and new_first_name != user.first_name:
            user.first_name = new_first_name
            updated = True

        if new_last_name and new_last_name != user.last_name:
            user.last_name = new_last_name
            updated = True

        if new_email and new_email != user.email:
            user.email = new_email
            updated = True

        profile_picture = request.FILES.get('profile_picture', None)
        if profile_picture:
            user.profile_picture = profile_picture
            updated = True

        if updated:
            user.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.info(request, 'No changes made to your profile.')

    return render(request, 'accounts/profile.html', {'user': user})

def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('confirm_password')
            first_name = request.POST.get('first-name')
            last_name = request.POST.get('last-name')
            profile_picture = request.POST.get('profile_picture') 
            organisation_id = request.POST.get('organisation')  # organisation comes from select

            if not all([email, password, password_confirm, first_name, last_name]):
                print("not all fields filled")
                messages.error(request, "Please fill in all required fields.")
                organisations = Organisation.objects.all()
                return render(request, 'accounts/register.html', {'organisations': organisations})

            if password != password_confirm:
                print("passwords do not match")
                return JsonResponse({'success': False, 'message': 'Something went wrong. Please try again.'}) 

            if User.objects.filter(email=email).exists():
                print("user already exists")
                return JsonResponse({'success': False, 'message': 'Something went wrong. Please try again.'})
            
            organisation = None
            if organisation_id:
                try:
                    organisation = Organisation.objects.get(org_id=organisation_id)
                except Organisation.DoesNotExist:
                    print("organisation does not exist")
                    return JsonResponse({'success': False, 'message': 'Organisation does not exist.'})

            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture or None,
                organisation=organisation
            )
            user.set_password(password)
            user.save()
            return JsonResponse({'success': True, 'redirect': reverse('accounts:login')})

        # For GET requests, fetch all organisations and pass them to the template
        organisations = Organisation.objects.all()
        return render(request, 'accounts/register.html', {'organisations': organisations})
    else:
        return redirect(reverse('dashboard:index'))

def settings(request):
    return render(request,'accounts/settings.html')
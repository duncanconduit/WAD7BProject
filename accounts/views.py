from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy

# Login view (using Django built-in LoginView)
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("profile")  # Redirect after successful login

# Logout view
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")  # Redirect to login page after logout

# Registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            messages.success(request, "Registration successful!")
            return redirect("profile")
        else:
            messages.error(request, "Registration failed, please check the input information")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# User profile page (requires login)
@login_required
def profile(request):
    return render(request, "accounts/profile.html")

# Settings page (requires login)
@login_required
def settings(request):
    return render(request, "accounts/settings.html")

# Password reset view
class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("login")

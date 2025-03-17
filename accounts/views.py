from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy

# 登录视图（使用 Django 内置的 LoginView）
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("profile")  # 登录成功后跳转

# 登出视图
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")  # 退出后跳转到登录页面

# 注册视图
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 自动登录
            messages.success(request, "注册成功！")
            return redirect("profile")
        else:
            messages.error(request, "注册失败，请检查输入信息")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# 用户个人资料页（需要登录）
@login_required
def profile(request):
    return render(request, "accounts/profile.html")

# 设置页面（需要登录）
@login_required
def settings(request):
    return render(request, "accounts/settings.html")

# 密码重置
class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("login")
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy

# 登录视图（使用 Django 内置的 LoginView）
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    success_url = reverse_lazy("profile")  # 登录成功后跳转

# 登出视图
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")  # 退出后跳转到登录页面

# 注册视图
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 自动登录
            messages.success(request, "注册成功！")
            return redirect("profile")
        else:
            messages.error(request, "注册失败，请检查输入信息")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# 用户个人资料页（需要登录）
@login_required
def profile(request):
    return render(request, "accounts/profile.html")

# 设置页面（需要登录）
@login_required
def settings(request):
    return render(request, "accounts/settings.html")

# 密码重置
class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("login")

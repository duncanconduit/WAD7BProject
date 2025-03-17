from django.urls import path
from .views import UserLoginView, UserLogoutView, register, profile, settings, UserPasswordResetView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("settings/", settings, name="settings"),
    path("password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
]

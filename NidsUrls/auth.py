from django.urls import path
from NidsViews.auth import (
    update_profile,
    get_profile,
    register,
    login,
    UserExists,
)

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("profile/update/", update_profile, name="update_profile"),
    path("profile/get/", get_profile, name="get_profile"),
    path("isUser", UserExists.as_view()),
]

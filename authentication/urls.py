from django.urls import path

from . import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("users/", views.user_list, name="user_list"),
    path(
        "users/<int:user_id>/",
        views.user_detail,
        name="user_detail",
    ),
]
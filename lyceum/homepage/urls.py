from django.urls import path

from homepage import views


app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("coffee/", views.coffee_endpoint, name="coffee"),
    path("echo/", views.echo, name="echo"),
    path("echo/submit/", views.echo_submit, name="echo_submit"),
    path("profile/<int:pk>/", views.profile, name="profile"),
]

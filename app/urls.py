from .views import *
from django.urls import path

app_name= "app"

urlpatterns = [
    path('', landing, name="landing_page"),

    path("register/",register, name = "register"),
    path("signin/", login_attepmt , name = "signin"),
    path("home/", home, name= "home"),
]
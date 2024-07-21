from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.models import User
# Create your views here.


def login_view(request:HttpRequest):

    user = User.objects

    return render(request,"user/login.html")

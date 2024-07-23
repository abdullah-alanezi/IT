from django.shortcuts import render

from django.http import HttpRequest

from .models import MaintenanceRequest
# Create your views here.


def support_request(request:HttpRequest):

    return render(request,"itsupport/support_request.html")


def user_request_view(request:HttpRequest):

    user_request = MaintenanceRequest.objects.all()

    

    return render(request,"itsupport/user_request.html",{"users_requests":user_request})


def my_order(request:HttpRequest):

    return render(request,"itsupport/my_order.html")





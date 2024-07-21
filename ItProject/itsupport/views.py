from django.shortcuts import render

from django.http import HttpRequest
# Create your views here.


def support_request(request:HttpRequest):

    return render(request,"itsupport/support_request.html")

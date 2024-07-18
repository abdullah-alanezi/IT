from django.shortcuts import render,redirect
from django.http import HttpRequest


# Create your views here.


def it_help_veiw(request:HttpRequest):        
   
    return render(request,"main/it_help.html")


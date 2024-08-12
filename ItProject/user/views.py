from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
# Create your views here.


def login_view(request:HttpRequest):
    msg =None
    if request.user.is_authenticated:
        return redirect('main:home_view')
    else:
            if request.method =="POST":

                user = authenticate(username = request.POST["username"],password=request.POST["password"])

                if user:
                    login(request,user)
                    return redirect('main:home_view')
                else:
                     msg = "اسم المستخدم أو كلمة المرور خاطئة"

       

    return render(request,"user/login.html",{"msg":msg})


def logout_view(request:HttpRequest):
    
    if request.user.is_authenticated:
        logout(request)
        
        return redirect("user:login_view")



def add_user_view(request:HttpRequest):
     msg =None
     if request.user.is_authenticated and request.user.is_superuser:
          if request.method == "POST":
               
               try:
                user=User.objects.create_user(username=request.POST["username"],first_name=request.POST["first_name"],email=request.POST["email"],last_name=request.POST["last_name"],password=request.POST["password"])

                if "is_staff" in request.POST:
                        user.is_staff = True
                user.save()
                
               except: msg ="اسم المستخدم موجود بالفعل"
                    

               
     
     return render(request,"user/add_user.html",{"msg":msg})
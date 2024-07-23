from django.shortcuts import render,redirect

from django.http import HttpRequest

from .models import MaintenanceRequest,PrinterRequest
# Create your views here.


def support_request(request:HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_request =MaintenanceRequest(
                user=request.user,
                device_type=request.POST["device_type"],
                device_id=request.POST["device_id"],
                problem_description =request.POST["problem_description"],
                image = request.FILES["image"]
                )
            user_request.save()
            return redirect("itsupport:my_order")
    else:
        return redirect("user:login_view")


    return render(request,"itsupport/support_request.html")


def user_request_view(request:HttpRequest):

    user_request = MaintenanceRequest.objects.all()

    

    return render(request,"itsupport/user_request.html",{"users_requests":user_request})


def my_order(request:HttpRequest):

    return render(request,"itsupport/my_order.html")



def add_printer_request(request:HttpRequest):

    if request.user.is_authenticated:
        if request.method == "POST":
            user_request =PrinterRequest(
                user=request.user,
                printer_type=request.POST["printer_type"],
                printer_id=request.POST["printer_id"],
                image = request.FILES["image"],
                ink_id = request.POST["ink_id"]
                )
            user_request.save()
            return redirect("itsupport:my_order")
    else:
        return redirect("user:login_view")
    





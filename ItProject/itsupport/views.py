from django.shortcuts import render,redirect

from django.http import HttpRequest

from .models import MaintenanceRequest,PrinterRequest
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
# Create your views here.


def send_order_status_email(recipient_email):
    subject = 'حالة الطلب'
    message = 'طلبك تحت الإجراء.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]

    send_mail(subject, message, email_from, recipient_list)



def support_request(request:HttpRequest):
    msg=None
    user = User.objects.get(id=request.user.id)
    orders = MaintenanceRequest.objects.filter(user=user)
    is_there =True

    for order in orders:
        if order.status =='تحت الإجراء' or order.status =='مفتوح':
            is_there = False
            break
    
    print(is_there)
    if is_there:
    
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
    else:
        msg="لايمكنك رفع طلب اخر حتى يغلق طلبك"


    return render(request,"itsupport/support_request.html",{"msg":msg})



def user_request_view(request:HttpRequest):
    if not request.user.is_staff:
        return redirect("main:home_view")

    user_request = MaintenanceRequest.objects.all()
    ink_requests = PrinterRequest.objects.all()

    

    return render(request,"itsupport/user_request.html",{"users_requests":user_request,"ink_requests":ink_requests})


def my_order(request:HttpRequest):
    user = User.objects.get(id=request.user.id)
    my_order = MaintenanceRequest.objects.filter(user=user)
    
    

    return render(request,"itsupport/my_order.html",{"my_order":my_order})



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
    


    
def request_detail_view(request:HttpRequest,request_id):

    request_detail = MaintenanceRequest.objects.get(id=request_id)
    if request.user.is_staff:

        
        user_email=request_detail.user.email
        if request.method == "POST":
            
            recipient_email = user_email
            print(request_detail.user.email)

            send_order_status_email(recipient_email)
            
            request_detail.status = "تحت الإجراء"
            request_detail.save()
            return redirect("itsupport:request_detail_view",request_id)
            


    return render(request,"itsupport/request_detail.html",{"request_detail":request_detail})



def close_order(request:HttpRequest,request_id):

    request_detail = MaintenanceRequest.objects.get(id=request_id)
    if request.user.is_staff:

        
        
        if request.method == "POST":
            
            
            request_detail.status = "منتهي "
            request_detail.save()
            return redirect("itsupport:request_detail_view",request_id)
        



def on_work_view(request:HttpRequest):

    return render(request,"itsupport/on_work.html")



def done_work_view(request:HttpRequest):

    return render(request,"itsupport/done_work.html")







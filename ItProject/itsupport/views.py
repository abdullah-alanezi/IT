from django.shortcuts import render,redirect

from django.http import HttpRequest

from .models import MaintenanceRequest,PrinterRequest
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


def send_order_status_email(recipient_email):
    subject = 'حالة الطلب'
    message = 'طلبك تحت الإجراء.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]

    send_mail(subject, message, email_from, recipient_list)



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
    # class_name=None
    my_order = MaintenanceRequest.objects.filter(user=request.user)
    
    # for order in my_order:

    #     if order.status == "منتهي":
    #         class_name="badge badge-status badge-closed"
            
    #     elif order.status =="تحت الإجراء":
    #         class_name="badge badge-status badge-in-progress"
    #     elif order.status =="مفتوح":
    #         class_name="badge badge-status badge-open"

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

            request_detail.status = 'تحت الإجراء'
            request_detail.save
            return redirect("itsupport:request_detail_view",request_id)
            


    return render(request,"itsupport/request_detail.html",{"request_detail":request_detail})









from django.shortcuts import render,redirect

from django.http import HttpRequest

from .models import MaintenanceRequest,PrinterRequest,ItHelp,PrinterHelp,Chat
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
    
    
    if is_there:
    
        if request.user.is_authenticated:
            if request.method == "POST":
                user_request =MaintenanceRequest(
                    user=request.user,
                    device_type=request.POST["device_type"],
                    device_id=request.POST["device_id"],
                    problem_description =request.POST["problem_description"],
                    
                    )
                if "image" in request.FILES:
                    user_request.image =request.FILES["image"]
                    
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

    printer_order = PrinterRequest.objects.filter(user=user)
    
    

    return render(request,"itsupport/my_order.html",{"my_order":my_order,"printer_order":printer_order})



def add_printer_request(request:HttpRequest):

    if request.user.is_authenticated:
        if request.method == "POST":
            user_request =PrinterRequest(
                user=request.user,
                printer_type=request.POST["printer_type"],
                printer_id=request.POST["printer_id"],
                
                ink_id = request.POST["ink_id"]
                )
            if "image" in request.FILES:
                user_request.image = request.FILES["image"]
            user_request.save()
            return redirect("itsupport:my_order")
    else:
        return redirect("user:login_view")
    


    
def request_detail_view(request:HttpRequest,request_id):

    it_chat=None
    user_chat=None
    request_detail =None
    prenter_detail = None
    it_emp =None
    try:

            request_detail = MaintenanceRequest.objects.get(id=request_id)
            request_detail.user
            user_chat = Chat.objects.filter(user=request_detail.user)
            try:

                emp = ItHelp.objects.get(user_request=request_detail)
                it_chat = Chat.objects.filter(user=emp.it_employee)
            except:
                emp=None
    except:
            prenter_detail = PrinterRequest.objects.get(id=request_id)
            user_chat = Chat.objects.filter(user=prenter_detail.user)
            
            try:

                emp = PrinterHelp.objects.get(user_request_p=prenter_detail)
                it_chat = Chat.objects.filter(user=emp.it_employee)
            except:
                    emp=None
    if request.user.is_staff:

        try:
            user_email=request_detail.user.email
        except:
                user_email=prenter_detail.user.email
        if request.method == "POST":
            
            recipient_email = user_email
            try:
                it_emp = ItHelp(it_employee=request.user,user_request=request_detail)
                it_emp.save()
            except:
                    it_emp = PrinterHelp(it_employee=request.user,user_request_p=prenter_detail)
                    it_emp.save()
                

            send_order_status_email(recipient_email)
            try:
                request_detail.status = "تحت الإجراء"
                request_detail.save()
            except:
                    prenter_detail.status = "تحت الإجراء"
                    prenter_detail.save()

            return redirect("itsupport:request_detail_view",request_id)
            


    return render(request,"itsupport/request_detail.html",{"request_detail":request_detail,"prenter_detail":prenter_detail,"emp":emp,"user_chat":user_chat,"it_chat":it_chat})



def close_order(request:HttpRequest,request_id):
    request_detail =None
    prenter_detail = None

    try:

        request_detail = MaintenanceRequest.objects.get(id=request_id)
    except:
        prenter_detail = PrinterRequest.objects.get(id=request_id)


    if request.user.is_staff:

        
        
        if request.method == "POST":
            
            
            try:
                request_detail.status = 'منتهي'
                request_detail.save()
            except:
                prenter_detail.status = 'منتهي'
                prenter_detail.save()
            
            chat=Chat.objects.get(user=request.user)
            chat.delete()
            return redirect("itsupport:done_work_view")
        



def on_work_view(request:HttpRequest):

    work_on =MaintenanceRequest.objects.filter(status='تحت الإجراء')

    return render(request,"itsupport/on_work.html",{"work_on":work_on})



def done_work_view(request:HttpRequest):

    done_work =MaintenanceRequest.objects.filter(status="منتهي")


    return render(request,"itsupport/done_work.html",{"done_works":done_work})




def chating(request:HttpRequest,request_id):
    chat = None
    user_request=None
    it_employee =None
    try:
        user_request = MaintenanceRequest.objects.get(id=request_id)
        it = ItHelp.objects.get(user_request=user_request) 
        it_employee = it.it_employee
    except:
         user_request = PrinterRequest.objects.get(id=request_id)
         it = PrinterHelp.objects.get(user_request_p=user_request) 
         it_employee = it.it_employee
        


    user_req = user_request.user
    if request.user.is_authenticated:
        if request.method =="POST":
             if request.user == user_req:
                chat=Chat(user=user_req,content=request.POST["content"])
                chat.save()
             else:
                chat=Chat(user=it_employee,content=request.POST["content"])
                chat.save()
             

        return redirect("itsupport:request_detail_view",request_id)


     






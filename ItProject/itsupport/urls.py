from django.urls import path
from .import views
app_name ="itsupport"


urlpatterns =[
    path("support/request/",views.support_request, name="support_request"),
    path("user/request/",views.user_request_view,name="user_request_view"),
    path("my/order/",views.my_order,name="my_order"),
    path("add/prenter/request",views.add_printer_request,name="add_printer_request"),
    path("request/detail/<request_id>",views.request_detail_view,name="request_detail_view"),
    path("close/order/<request_id>",views.close_order,name="close_order"),
    path("on/workv/",views.on_work_view ,name="on_work_view"),
    path("done/work/",views.done_work_view,name="done_work_view"),
    path("chating/<request_id>/",views.chating,name="chating")
]

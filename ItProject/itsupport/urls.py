from django.urls import path
from .import views
app_name ="itsupport"


urlpatterns =[
    path("support/request/",views.support_request, name="support_request"),
    path("user/request/",views.user_request_view,name="user_request_view"),
]

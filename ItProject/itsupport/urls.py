from django.urls import path
from .import views
app_name ="itsupport"


urlpatterns =[
    path("support_request/",views.support_request, name="support_request"),
]

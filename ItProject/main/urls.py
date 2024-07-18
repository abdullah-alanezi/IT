from django.urls import path
from .import views
appp_name = "main"


urlpatterns =[
    path("", views.it_help_veiw,name="it_help"),

]
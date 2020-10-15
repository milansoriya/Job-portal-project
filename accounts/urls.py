from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.login,name='login'),
    path("Employee_registration",views.Employee_registration,name='Employee_registration'),
    path("Employeer_registration",views.Employeer_registration,name='Employeer_registration'),
    path("Company_logout",views.Company_logout,name='Company_logout'),
    path("User_logout",views.User_logout,name='User_logout'),
    path("home",include('jobportal.urls')),
    path("Company_home",include('jobportal.urls')),
]

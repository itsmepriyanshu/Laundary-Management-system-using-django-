from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='index.html', permanent=True)),
    path("index.html", views.index, name="index"),
    path('UserLogin.html', views.UserLogin, name="UserLogin"), 
    path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),
    path('Register.html', views.Register, name="Register"), 
    path('RegisterAction', views.RegisterAction, name="RegisterAction"),
    path('LaundryService', views.LaundryService, name="LaundryService"),
    path('LaundryServiceAction', views.LaundryServiceAction, name="LaundryServiceAction"),	 
    path('YoloGraph', views.YoloGraph, name="YoloGraph"),
    path('ViewLaundry', views.ViewLaundry, name="ViewLaundry"),
    path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
    path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),
    path('ViewCustomers', views.ViewCustomers, name="ViewCustomers"),
    path('ViewOrderStatus', views.ViewOrderStatus, name="ViewOrderStatus"),
    path('UploadImageAction', views.UploadImageAction, name="UploadImageAction"),
    path('WriteDescription', views.WriteDescription, name="WriteDescription"), 
    path('WriteDescriptionAction', views.WriteDescriptionAction, name="WriteDescriptionAction"),
    path('About.html', views.About, name="About"),
    path('Contact.html', views.Contact, name="Contact"),
    path('ContactAction', views.ContactAction, name="ContactAction"),
]
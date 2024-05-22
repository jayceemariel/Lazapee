"""
URL configuration for Lazapee project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls, name='custom_admin'),
    path('', views.login, name='Login'),
  
    #For Accounts Requires the UNIQUE ID of the Class
    path('Sign-up',views.signup, name='sign-up_view'),
   
   #Manage Account Stuff
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('manage_account/<int:pk>/', views.manage_account, name='manage_account'),
    path('account_deleted/<int:pk>/', views.delete_account, name='delete_account'),

    #Viewing of Employee
    path('view_employee/<int:pk>/', views.employee, name='employee'),
    path('add_employee/<str:id>/', views.add_employee, name='add_employee'),
    path('update_employee/<str:id>/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete_employee/<str:id>/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('overtime_pay/<str:pk>/<int:id>/', views.overtime, name='overtime'),
    path('reset_overtime/<str:id>/<int:pk>/', views.reset_overtime, name='rovertime'),
    path('delete_all_employee/<str:id>/', views.delete_all_employees, name='delete_all_employee'),

    #Pay-slips
    path('view_payslips/<str:id>/<int:pk>/', views.view_payslip, name='view_payslip'),
    path('payslips/<int:pk>/', views.pay_slip, name='payslips'),
    path('delete_all_payslips/<str:id>', views.delete_payslips, name='del_payslips'),
    
]


"""staffmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('', views.index, name='index'),
    path('management/', views.management_options, name='management_options'),
    path('clock-in/', views.clock_in, name='clock_in'), 
    path('clock-out/', views.clock_out, name='clock_out'),
    path('employee-info/', views.employee_information, name='employee_information'),
    path('schedule/', views.schedule, name='schedule'),
    path('request-schedule-change/', views.request_schedule_change, name='request_schedule_change'),
    path('update-employee/', views.update_employee, name='update_employee'),
    path('about/', views.about, name='about'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('remove-employee/', views.remove_employee, name='remove_employee'),
]

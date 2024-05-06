from django.contrib import admin
from .models import Shift, Schedule, Employee

admin.site.register(Schedule)
admin.site.register(Employee)
admin.site.register(Shift)
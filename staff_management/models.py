from django.db import models
from datetime import datetime

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    tenure = models.IntegerField()
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    wage = models.DecimalField(max_digits=8, decimal_places=2)
    avg_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2)

class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    shift_start = models.TimeField()
    shift_end = models.TimeField()

class Shift(models.Model):
    employee = models.ForeignKey('staff_management.Employee', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(default=datetime.now().time())
    end_time = models.TimeField(null=True, blank=True)  # Nullable end_time

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.start_time} to {self.end_time}"

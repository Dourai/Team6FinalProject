from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    tenure = models.IntegerField()
    department = models.CharField(max_length=100)
    wage = models.DecimalField(max_digits=8, decimal_places=2)
    avg_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2)

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20)
    tenure = models.IntegerField()
    department = models.CharField(max_length=100)
    wage = models.DecimalField(max_digits=8, decimal_places=2)
    avg_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2)

class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    shift_start = models.TimeField()
    shift_end = models.TimeField()

class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee.name}'s shift on {self.date}"
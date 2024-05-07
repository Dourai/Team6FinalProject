from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, name, tenure, department, wage, avg_hours_per_week, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            name=name,
            tenure=tenure,
            department=department,
            wage=wage,
            avg_hours_per_week=avg_hours_per_week,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, tenure, department, wage, avg_hours_per_week, password):
        user = self.create_user(
            username,
            name=name,
            tenure=tenure,
            department=department,
            wage=wage,
            avg_hours_per_week=avg_hours_per_week,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Employee(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    tenure = models.IntegerField()
    department = models.CharField(max_length=100)
    wage = models.DecimalField(max_digits=8, decimal_places=2)
    avg_hours_per_week = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'tenure', 'department', 'wage', 'avg_hours_per_week']

    def __str__(self):
        return self.username

class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    shift_start = models.TimeField()
    shift_end = models.TimeField()

class Shift(models.Model):
    employee = models.ForeignKey('staff_management.Employee', on_delete=models.CASCADE, related_name='shifts')
    date = models.DateField()
    start_time = models.TimeField(default=datetime.now().time())
    end_time = models.TimeField(null=True, blank=True)  # Nullable end_time

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.start_time} to {self.end_time}"

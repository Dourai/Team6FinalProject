from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from staff_management.forms import LoginForm
from .models import Employee, Shift
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def index(request):
    return redirect('/home')

@login_required(login_url='/login')
def home(request):
    my_list = [
        ('Clock in', '/clock-in', 1),
        ('Clock out', '/clock-out', 2),
        ('Schedule', '/schedule', 3),
        ('Employee Information', '/employee-info', 4),
        ('Management Options', '/management', 5),
    ]
    return render(request, 'index.html', {'my_list': my_list})

@login_required(login_url='/login')
def management_options(request):
    return render(request, 'managementoptions.html')

@login_required(login_url='/login')
def clock_in(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if employee.password == password:
                # Clock in the employee
                Shift.objects.create(employee=employee, date=date.today(), start_time=timezone.now())
                messages.success(request, 'You have successfully clocked in.')
                return redirect('clock_out')  # Redirect to clock-out page after successful clock-in
            else:
                messages.error(request, 'Incorrect password.')
        except Employee.DoesNotExist:
            messages.error(request, 'Employee not found.')
    
    return render(request, 'clock_in.html')

@login_required(login_url='/login')
def clock_out(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if employee.password == password:
                current_shift = Shift.objects.filter(employee=employee, date=date.today()).latest('start_time')
                current_shift.end_time = datetime.now().time()
                current_shift.save()
                messages.success(request, 'You have successfully clocked out.')
                return redirect('/home')  # Redirect to home page after successful clock-out
            else:
                messages.error(request, 'Invalid password.')
        except Employee.DoesNotExist:
            messages.error(request, 'Employee not found.')
    
    error_messages = [str(message) for message in messages.get_messages(request)]  # Convert messages to a list of strings
    return render(request, 'clock_out.html', {'error_message': error_messages})

@login_required(login_url='/login')
def employee_information(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if employee.password == password:
                context = {
                    'employee': employee,
                    'found': True
                }
            else:
                context = {
                    'found': False,
                    'error_message': 'Incorrect password.'
                }
        except Employee.DoesNotExist:
            context = {
                'found': False,
                'error_message': 'Employee not found.'
            }
        
        return render(request, 'employee_info.html', context)

    return render(request, 'employee_info.html')

@login_required(login_url='/login')
def schedule(request):
    # Sample data
    schedule_data = {
        "2024-04-29": "Work",
        "2024-05-01": "Work",
        "2024-05-03": "Work",
        "2024-05-05": "Unavailable"
    }

    context = {
        'title': 'Schedule',
        'schedule_data': schedule_data,
        'request_change_url': '/request-schedule-change',  # URL for requesting schedule change
    }
    return render(request, 'schedule.html', context)

def request_schedule_change(request):
    # Placeholder for handling schedule change requests
    if request.method == 'POST':
        # Process the form data for schedule change request
        employee_id = request.POST.get('employee_id')
        new_schedule_date = request.POST.get('new_schedule_date')
        reason = request.POST.get('reason')

        return redirect('/schedule')

    context = {
        'title': 'Request Schedule Change',
    }
    return render(request, 'request_schedule_change.html', context)

@login_required(login_url='/login')
def update_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if 'update' in request.POST:
                # Update employee details
                employee.name = request.POST.get('name')
                employee.tenure = request.POST.get('tenure')
                employee.department = request.POST.get('department')
                employee.wage = request.POST.get('wage')
                employee.avg_hours_per_week = request.POST.get('avg_hours')
                employee.save()
                return redirect('home')  # Redirect to home page after successful update
            return render(request, 'update_employee.html', {'employee': employee})
        except Employee.DoesNotExist:
            error_message = 'Employee with ID {} does not exist.'.format(employee_id)
            return render(request, 'update_employee.html', {'error_message': error_message})
    else:
        return render(request, 'update_employee.html')


def add_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')
        if Employee.objects.filter(employee_id=employee_id).exists():
            return render(request, 'add_employee.html', {'error': 'Employee with this ID already exists.'})
        else:
            name = request.POST.get('name')
            tenure = request.POST.get('tenure')
            department = request.POST.get('department')
            wage = request.POST.get('wage')
            avg_hours_per_week = request.POST.get('avg_hours_per_week')
            
            new_employee = Employee(
                name=name,
                employee_id=employee_id,
                password=password,
                tenure=tenure,
                department=department,
                wage=wage,
                avg_hours_per_week=avg_hours_per_week
            )
            new_employee.save()
            return render(request, 'add_employee.html', {'success': True})
    return render(request, 'add_employee.html')

def remove_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        if Employee.objects.filter(employee_id=employee_id).exists():
            Employee.objects.filter(employee_id=employee_id).delete()
            return render(request, 'remove_employee.html', {'success': True})
        else:
            return render(request, 'remove_employee.html', {'error': 'Employee with this ID does not exist.'})
    return render(request, 'remove_employee.html')

def about(request):
    return render(request, 'about.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print('aaaaa', form.is_valid())
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            password = form.cleaned_data.get('password')
            employee = authenticate(request, username=employee_id, password=password)
            if employee is not None:
                login(request, employee)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid employee ID or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
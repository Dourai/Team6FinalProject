from django.shortcuts import render, redirect
from .models import Employee, Schedule, Shift

def index(request):
    return redirect('/home')

def home(request):
    my_list = [
        ('Clock in', '/clock-in', 1), 
        ('Clock out', '/clock-out', 2),
        ('Schedule', '/schedule', 3),
        ('Employee Information', '/employee-info', 4),
        ('Management Options', '/management', 5),
    ] 
    return render(request, 'index.html', {'my_list': my_list})

def management_options(request):
    return render(request, 'managementoptions.html')

def clock_in(request):
    success = False
    if request.method == 'POST':
        success = True  # For demonstration purposes
    return render(request, 'clock_in.html', {'success': success})

def clock_out(request):
    success = False
    if request.method == 'POST':
        success = True  # For demonstration purposes
    return render(request, 'clock_out.html', {'success': success})

def employee_information(request):
    # Sample data for demonstration
    sample_employee = {
        'name': 'Thi Nguyen',
        'employee_id': '12345',
        'tenure': '2 years',
        'department': 'Front-end',
        'wage': '$20 per hour',
        'avg_hours_per_week': '40 hours'
    }
    
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        # Check if the provided employee ID matches the sample employee
        if employee_id == sample_employee['employee_id']:
            # Employee found, proceed to display their information
            context = {
                'employee': sample_employee,
                'found': True  # You can use this flag to indicate that the employee was found
            }
            return render(request, 'employee_info.html', context)
        else:
            # Employee not found, display an error message or handle the situation accordingly
            context = {
                'found': False  # You can use this flag to indicate that the employee was not found
            }
            return render(request, 'employee_info.html', context)

    return render(request, 'employee_info.html')

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

def update_employee(request):
    return render(request, 'update_employee.html')

def about(request):
    return render(request, 'about.html')

def add_employee(request):
    return render(request, 'add_employee.html')

def remove_employee(request):
    return render(request, 'remove_employee.html')


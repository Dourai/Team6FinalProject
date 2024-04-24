from django.shortcuts import render, redirect
from .models import Employee

def index(request):
    return redirect('/home')

def home(request):
    context = {
        'title': 'Home Page',
        'heading': 'Staff Management System',
        'content': 'The Staff Management System is designed to streamline employee management processes within an organization. It provides functionality for employees to access work-related information such as schedules, wages, tenure, and department details. Additionally, it facilitates clocking in and out for shifts.',
    }
    return render(request, 'index.html', context)

def about(request):
    my_list = [
        ('Clock in', '/clock-in', 1), 
        ('Clock out', '/clock-out', 2),
        ('Schedule', '/schedule', 3),
        ('Employee Information', '/employee-info', 4),
        ('Management Options', '/management', 5),
    ] 
    return render(request, 'about.html', {'my_list': my_list})

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



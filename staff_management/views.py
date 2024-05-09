from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from staff_management.forms import LoginForm
from .models import Employee, Shift
from datetime import datetime, date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import EmployeeNameUpdateForm, EmployeePasswordUpdateForm


def index(request):
    return redirect('/home')

@login_required
def home(request):
    my_list = [
        ('Clock in', '/clock-in', 1),
        ('Clock out', '/clock-out', 2),
        ('Schedule', '/schedule', 3),
        ('Employee Information', '/employee-info', 4),
    ]
    if request.user.is_superuser:
        my_list.append(('Management Options', '/admin/staff_management/employee/', 5))

    return render(request, 'index.html', {'my_list': my_list})

@login_required
def management_options(request):
    return render(request, 'managementoptions.html')

# This view will handle the clock in functionality
@login_required
def clock_in(request):
    if request.method == 'POST':
        shift, created = request.user.shifts.get_or_create(date=date.today())

        # Check if the shift was created, if it was, set the start time to the current time
        # if it wasn't, means the user has already clocked in today
        if created:
            shift.start_time = timezone.now()
            shift.save()
            messages.success(request, 'You have successfully clocked in.')
            return redirect('clock_out')
        else:
            messages.error(request, 'You have already clocked in today.')

    return render(request, 'clock_in.html', {'messages': messages.get_messages(request)})


@login_required
def clock_out(request):
    if request.method == 'POST':
        try:
            # Get the shift for today, if it exists
            shift = request.user.shifts.get(date=date.today())
            if shift.end_time is None:
                shift.end_time = timezone.now()
                shift.save()
                messages.success(request, 'You have successfully clocked out.')
            else: # If the end time is not None, means the user has already clocked out
                messages.error(request, 'You have already clocked out today.')
        except Shift.DoesNotExist:
            messages.error(request, 'You have not clocked in today.')

    return render(request, 'clock_out.html', {'messages': messages.get_messages(request)})


@login_required
def employee_information(request):
    return render(request, 'employee_info.html')

@login_required
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

@login_required
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

# This view handles the login functionality
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            password = form.cleaned_data.get('password')
            # We are using Django's built-in authenticate method to check if the employee ID and password are correct
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


# We only want superusers to be able to add employees
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_employee(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = UserCreationForm()
    return render(request, 'add_employee.html', {'form': form})

# This view is used to update employee information
@login_required
def employee_information_update(request):
    if request.method == 'POST':
        try:
            employee = Employee.objects.get(pk=request.user.id)
            employee.name = request.POST.get('name')
            if request.POST.get('password'):
                employee.set_password(request.POST.get('password'))

            employee.save()
            return redirect('employee_information')
        except Employee.DoesNotExist:
            return render(request, 'employee_info_update.html', {'error_message': 'Something went wrong. Please try again.'})
    return render(request, 'employee_info_update.html')

# We don't want to use the default Django login page, so we redirect to our custom login page
def go_to_custom_login(request):
    return redirect('/accounts/login')

# We don't want to use the default Django logout page, so we redirect to our custom logout page
def go_to_custom_logout(request):
    return redirect('/accounts/logout')


# We use Django's class-based views for updating employee information
class EmployeeNameUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeNameUpdateForm
    template_name = 'employee_name_update.html'
    success_url = reverse_lazy('employee_information')  # Redirect to employee information page after successful update


# We use Django's class-based views for updating employee password
class EmployeePasswordUpdateView(UpdateView):
    model = Employee
    form_class = EmployeePasswordUpdateForm
    template_name = 'employee_password_update.html'
    success_url = reverse_lazy('employee_information')  # Redirect to employee information page after successful update

    def form_valid(self, form):
        # We need to set the password for the user
        # the set_password method will hashes the plain password before saving it
        form.instance.user = self.request.user
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)

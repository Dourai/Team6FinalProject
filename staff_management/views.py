from django.shortcuts import render
from django.shortcuts import redirect

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
        ('Clock in', '', 1), 
        ('Clock out', '', 2),
        ('Schedule', '', 3),
        ('Employee Information', '', 4),
        ('Management Options', '', 5),
    ] 
    return render(request, 'about.html', {'my_list': my_list})


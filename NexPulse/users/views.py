from django.http import HttpResponse
from django.shortcuts import render, redirect

from users.models import UserDetails


def signup(request):
    if request.method == 'POST':
        req_email_id = request.POST['email']
        req_password = request.POST['password']
        req_confirm_password = request.POST['confirm_password']
        if req_confirm_password != req_password:
            print('password and confirmation do not match')
            return render(request, 'users/invalidPassword.html')
        user = UserDetails.objects.create(
            email_id=req_email_id,
            password=req_password
        )
        return redirect(login)
    return render(request, 'users/signup.html')


def login(request):
    if request.method == 'POST':
        login_email = request.POST['login_email']
        login_password = request.POST['login_password']

        # Check if the email exists in the Student table
        user1 = UserDetails.objects.filter(email_id=login_email).first()
        if not user1:
            return HttpResponse('Invalid email. Please register.')

        # Check if the password exists in the StudentPassword table for the corresponding student_id
        user1_password = user1.password
        if user1_password == login_password:
            # If login is successful, redirect to the course_selection page
            return redirect(home)
        else:
            return HttpResponse('Invalid password. Please try again.')

    return render(request, 'users/login.html')


def home(request):
    return render(request, 'users/home.html')


def logout(request):
    return render(request, 'users/login.html')

from django.shortcuts import render, redirect


def signup(request):
    return render(request, 'users/signup.html')


def login(request):
    return render(request, 'users/login.html')


def home(request):
    return render(request, 'users/home.html')


def logout(request):
    return render(request, 'users/login.html')

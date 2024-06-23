from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(email=email, password=password)
            return JsonResponse({'message': 'User created successfully'}, status=201)
        else:
            return JsonResponse({'message': 'User already exists'}, status=400)
    else:
        return HttpResponse("This endpoint only accepts POST requests.", status=405)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        return HttpResponse("This endpoint only accepts POST requests.", status=405)

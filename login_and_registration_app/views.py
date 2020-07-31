from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'index.html')

def registration(request):
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    errors = User.objects.validator_register(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(firstName=firstName, lastName=lastName, email=email, password=pw_hash)
        request.session['userid'] = user.id
        return redirect('/dashboard/')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=request.POST['email'])
    errors = User.objects.validator_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    elif user:
        logged_user = user[0]
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid password")
    return redirect('/')

def endSession(request):
    del request.session['userid']
    return redirect('/')

@csrf_exempt
def check_email_exists(request):
    email=request.POST.get("email")
    user_obj=User.objects.filter(email=email)
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
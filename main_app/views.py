from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):

    if not 'userid' in request.session:
        return redirect('/')
    else:
        currentUser = User.objects.get(id=request.session['userid'])
        context = {
            'user': currentUser,
        }
    return render(request, 'homepage.html', context)

def create(request):
    user = User.object.get(id = request.session['user_id'])
    title = request.POST['title']
    start = request.POST['start']
    end = request.POST['end']
    working = request.POST['working']
    notes = request.POST['message']
    Project.objects.create()
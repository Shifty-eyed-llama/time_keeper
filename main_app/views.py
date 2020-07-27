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
            'all_projects' : Project.objects.all(),
        }
    return render(request, 'homepage.html', context)

def new(request):
    context = {
        'users' : User.objects.all()
    }
    return render(request, 'create.html', context)

def create(request):
    user = User.objects.get(id = request.session['userid'])
    title = request.POST['title']
    start = request.POST['start']
    end = request.POST['end']
    working = request.POST['working']
    notes = request.POST['message']
    new_proj = Project.objects.create(title = title, start_date = start, end_date = end, created_by = user)
    # if notes:
    #     new_proj.messages.add(notes)
    if working:
        new_proj.working.add(working)
    return redirect('/dashboard')

def delete(request, proj_id):
    this_project = Project.objects.get(id = proj_id)
    this_project.delete()
    return redirect('/dashboard')
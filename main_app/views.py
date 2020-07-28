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
        'users' : User.objects.all(),
        'user' : User.objects.get(id = request.session['userid'])
    }
    return render(request, 'create.html', context)

def create(request):
    user = User.objects.get(id = request.session['userid'])
    title = request.POST['title']
    start = request.POST['start']
    end = request.POST['end']
    notes = request.POST['message']
    new_proj = Project.objects.create(title = title, start_date = start, end_date = end, created_by = user)
    return redirect('/dashboard')

def delete(request, proj_id):
    this_project = Project.objects.get(id = proj_id)
    this_project.delete()
    return redirect('/dashboard')
def detail(request, proj_id):
    this_project = Project.objects.get(id=proj_id)
    this_user = User.objects.get(id= request.session['userid'])
    context = {
        'project' : this_project,
        'user' : this_user,
        'all_user' : User.objects.all(),
    }
    return render(request, 'view.html', context)

def remove(request, proj_id):
    this_project = Project.objects.get(id=proj_id)
    this_user = User.objects.get(id= request.POST['userid'])
    this_project.working.remove(this_user)
    return redirect

def edit(request, proj_id):
    this_project = Project.objects.get(id=proj_id)
    user = User.objects.get(id = request.session['userid'])
    title = request.POST['title']
    start = request.POST['start']
    end = request.POST['end']
    working = request.POST['working']
    notes = request.POST['message']
    this_project.title = title
    this_project.start_date = start
    this_project.end_date = end
    this_project.save()
    for value in request.POST['working']:
        this_user = User.objects.get(id=request.POST['working'])
        this_project.working.add(this_user)
    return redirect('/dashboard')

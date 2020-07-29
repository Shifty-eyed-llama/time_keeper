from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime, timezone
from django.db.models import F

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
    # notes = request.POST['message']
    new_proj = Project.objects.create(title = title, start_date = start, end_date = end, created_by = user)
    return redirect('/dashboard')

def delete_project(request, proj_id):
    this_project = Project.objects.get(id = proj_id)
    this_project.delete()
    return redirect('/dashboard')
def detail(request, proj_id):
    this_user = User.objects.get(id= request.session['userid'])
    this_project = Project.objects.get(id=proj_id)
    time = Timekeeper.objects.filter(proj_time=this_project) # only project times (hopefully)
    last_time = Timekeeper.objects.last()
    varsum = 0
    for i in time:
        varsum += i.entire_time
    context = {
        'project' : this_project,
        'user' : this_user,
        'all_user' : User.objects.all(),
        'proj_times' : time,
        'last_time' : last_time,
        'varsum' : varsum,
    }
    return render(request, 'view.html', context)

def clockin(request, proj_id):
    this_project = Project.objects.get(id=proj_id)
    user = User.objects.get(id=request.session['userid'])
    now = datetime.now(timezone.utc)
    time = Timekeeper.objects.create(clock_in=now, clock_out=now, entire_time = int(0), users_time=user, proj_time = this_project, is_working=True)
    # time_id = request.session['timeid']
    Timekeeper.objects.update(total_time=F('clock_out') - F('clock_in'))
    return redirect('/dashboard/view/'+str(proj_id))

def clockout(request, proj_id):
    user = User.objects.get(id=request.session['userid'])
    now = datetime.now(timezone.utc)
    this_proj = Project.objects.get(id = proj_id)
    this_time = Timekeeper.objects.last()
    time = this_time.users_time # ummm... i dont even know... may have to modify
    this_time.clock_out = now
    this_time.is_working = False
    this_time.save()
    Timekeeper.objects.update(total_time=F('clock_out') - F('clock_in'))
    Timekeeper.objects.update(entire_time=F('total_time'))
    return redirect('/dashboard/view/'+str(proj_id))

def remove_user(request, proj_id):
    this_project = Project.objects.get(id=proj_id)
    this_user = User.objects.get(id= request.POST['userid'])
    this_project.working.remove(this_user)
    return redirect('/dashboard/view/'+str(proj_id))

def delete_time(request, time_id):
    time = Timekeeper.objects.get(id=time_id)
    time.delete()
    return redirect('/dashboard')

def edit_project(request, proj_id):
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


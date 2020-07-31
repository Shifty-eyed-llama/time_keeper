from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime, timezone
from django.db.models import F
import pytz
import uuid

# Create your views here.

def index(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        currentUser = User.objects.get(id=request.session['userid'])
        context = {
            'user': currentUser,
            'all_projects' : Project.objects.all(),
            'timezones': pytz.common_timezones,
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
    last_proj = Project.objects.last()
    user.projects_assigned_to.add(last_proj)
    if notes:
        Message.objects.create(note = notes , created_by = user, project = new_proj)
    return redirect('/dashboard')

def delete_project(request, proj_id):
    this_project = Project.objects.get(id = proj_id)
    this_project.delete()
    return redirect('/dashboard')
def detail(request, proj_id):
    this_user = User.objects.get(id= request.session['userid'])
    this_project = Project.objects.get(id=proj_id)
    time = Timekeeper.objects.filter(proj_time=this_project) # only project times (hopefully)
    notes = this_project.notes.all()
    last_time = Timekeeper.objects.last()
    varsum = 0
    for i in time:
        varsum += i.entire_time
    context = {
        'notes' : notes,
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
    notes = request.POST['message']
    this_project.title = title
    this_project.start_date = start
    this_project.end_date = end
    this_project.save()
    if notes:
        Message.objects.create(note = notes , created_by = user, project = this_project)
    return redirect('/dashboard')
def new_note(request, proj_id):
    this_project = Project.objects.get(id=proj_id)

def view_profile(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['userid'])
        # user_projects = Project.objects.filter(user)
        context = {
            'user' : user,
            # 'user_projects' : user_projects,
        }
        return render(request, 'profile.html', context)

def create_post(request):
    subject = request.POST['subject']
    file_name = request.FILES["profile_picture"].name
    request.FILES['profile_picture'].name = "{}.{}".format(uuid.uuid4().hex, file_name.split(".")[-1])

    Picture.objects.create(subject = subject, file_name = file_name, image = request.FILES['profile_picture'], users_pic = User.objects.get(id = request.session['userid']))
    return redirect('/dashboard/profile')

    this_user = User.objects.get(id=request.session['userid'])
    Message.objects.create(
        note = request.POST['notes'], 
        created_by = this_user,
        project = this_project,
    )
    return redirect('/dashboard/view/' + str(proj_id))

def new_comment(request, proj_id):
    this_message = Message.objects.get(id=request.POST['message_id'])
    this_user = User.objects.get(id=request.session['userid'])
    Comment.objects.create(
        comments = request.POST['comments'], 
        user_comments = this_user,
        message_comments = this_message,
    )
    return redirect('/dashboard/view/' + str(proj_id))

def join_project(request, proj_id):
    this_user = User.objects.get(id=request.session['userid'])
    this_project = Project.objects.get(id=proj_id)
    this_project.projects_working_on.add(this_user)
    return redirect('/dashboard')

def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/dashboard')
    else:
        return render(request, 'homepage.html', {'timezones': pytz.common_timezones})
def archive(request, proj_id):
    project = Project.objects.get(id=proj_id)
    project.done = True
    project.save()
    return redirect('/dashboard')
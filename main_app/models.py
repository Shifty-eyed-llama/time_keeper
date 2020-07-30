from django.db import models
from login_and_registration_app.models import *
from django.utils.timezone import utc
from datetime import datetime


# Create your models here.

class ProjectManager(models.Manager):
    def project_validate(self, postData):
        errors = {}
        date = postData['start']
        end_date = postData['end']
        if date < str(datetime.date.today()):
            errors['start'] = ("The date cannot be in the past!")
        if end_date < date:
            errors['end'] = ("The end date must be after start date")
        return errors

class Project(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    created_by = models.ForeignKey(User, related_name = 'made_by', on_delete=models.CASCADE)
    projects_working_on = models.ManyToManyField(User, related_name = "projects_assigned_to")
    objects = ProjectManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    note = models.TextField(null=True)

    created_by = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='notes', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comments = models.TextField()

    user_comments = models.ForeignKey(User, related_name="comments_by_user", on_delete=models.CASCADE)
    message_comments = models.ForeignKey(Message, related_name="comments_on_message", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Timekeeper(models.Model):
    clock_in = models.DateTimeField(null=True)
    clock_out = models.DateTimeField(null=True)
    total_time = models.DurationField(null=True, blank=True)
    entire_time = models.FloatField(null=True)
    is_working = models.BooleanField(default=False)

    users_time = models.ForeignKey(User, related_name="time_of_user", on_delete=models.CASCADE)
    proj_time = models.ForeignKey(Project, related_name = 'time_of_project', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Picture(models.Model):
    subject = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="profile_images")

    users_pic = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

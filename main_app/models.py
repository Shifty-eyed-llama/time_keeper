from django.db import models
from login_and_registration_app.models import *
import datetime


# Create your models here.

class ProjectManaget(models.Manager):
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
    end_date = models.DateField()
    start_date = models.DateField()

    created_by = models.ForeignKey(User, related_name = 'made_by', on_delete=models.CASCADE)
    working = models.ManyToManyField(User, related_name = "working_on")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    note = models.TextField(null=True)

    created_by = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Time(models.Model):
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    total_time = datetime.timedelta()

    user = models.ForeignKey(User, related_name='time', on_delete=models.CASCADE)
    project = models.ForeignKey(Project,related_name='project_time', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
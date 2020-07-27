from django.db import models
from login_and_registration_app.models import *

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    end_date = models.DateTimeField()
    start_date = models.DateTimeField()

    created_by = models.ForeignKey(User, related_name = 'made_by', on_delete=models.CASCADE)
    working = models.ManyToManyField(User, related_name = "working_on")
    messages = models.ManyToManyField(User, related_name="messages")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
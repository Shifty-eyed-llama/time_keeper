from django.db import models
from login_and_registration_app.models import *
<<<<<<< HEAD

=======
>>>>>>> b4143a4cc65cdc868c328516a4f064b779d1d7e8

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    end_date = models.DateTimeField()
    Start_date = models.DateTimeField()

    created_by = models.ForeignKey(User, related_name = 'made_by')
    working = models.ManyToManyField(User, related_name = "working_on")
    messages = models.ManyToManyField(User, related_name="messages")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
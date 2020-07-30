from django.db import models
from login_and_registration_app.models import *
from django.utils.timezone import utc
from datetime import datetime

# Create your models here.

class ProjectManager(models.Manager):
    def project_validate(self, postData):
        errors = {}
        present = str(datetime.now())
        date = postData['start']
        end_date = postData['end']
        if len(postData['title']) < 2:
            errors['title'] = "Title must be at least 2 characters."
        # if len(postData['notes']) > 0 < 2:
        #     errors['notes'] = "Notes must be at least 2 characters."
        if len(postData['start']) < 10:
            errors['start'] = "Start date cannot be empty."
        elif date < present:
            errors['start'] = ("The date cannot be in the past!")
        if len(postData['end']) < 10:
            errors['end'] = "End date cannot be empty."
        elif end_date < date:
            errors['end'] = ("The end date must be after start date.")
        return errors

class Project(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    created_by = models.ForeignKey(User, related_name = 'made_by', on_delete=models.CASCADE)
    # working = models.ManyToManyField(User, related_name = "working_on")
    # notes = related Message
    objects = ProjectManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MessageManager(models.Manager):
    def message_validate(self, postData):

        errors = {}
        # if postData['notes'].isalpha() == False:
        #     errors['notes'] = "Message must be alphanumeric characters"
        if len(postData['notes']) < 1:
            errors['notes'] = "Message cannot be blank"
        return errors

class Message(models.Model):
    note = models.TextField(null=True)

    created_by = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='notes', on_delete=models.CASCADE)

    objects = MessageManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentManager(models.Manager):
    def comment_validate(self, postData):
        errors = {}
        # if postData['comments'].isalpha() == False:
        #     errors['comments'] = "Comment must be alphanumeric characters"
        if len(postData['comments']) < 1:
            errors['comments'] = "Comment cannot be blank"
        return errors

class Comment(models.Model):
    comments = models.TextField()

    user_comments = models.ForeignKey(User, related_name="comments_by_user", on_delete=models.CASCADE)
    message_comments = models.ForeignKey(Message, related_name="comments_on_message", on_delete=models.CASCADE)

    objects = CommentManager()

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
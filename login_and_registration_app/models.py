from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def validator_register(self, postData):
        errors = {}
        email = postData['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['firstName']) < 2:
            errors['firstName'] = "First name must be at least 2 characters"
        if postData['firstName'].isalpha() == False:
            errors['firstName2'] = "First name must contain only alphabetical characters"
        if len(postData['lastName']) < 2:
            errors['lastName'] = "Last name must be at least 2 characters"
        if postData['lastName'].isalpha() == False:
            errors['lastName2'] = "Last name must contain only alphabetical characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if User.objects.filter(email=email):
            errors['email2'] = "That email address already exists"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Your passwords do not match"
        if len(postData['password']) < 8:
            errors['password2'] = "Your password is too short"
        return errors

    def validator_login(self, postData):
        errors = {}
        email = postData['email']
        if not User.objects.filter(email=email):
            errors['email'] = "Could not find a matching email address"
        return errors


class User(models.Model):
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    # "users_time" R/T class Project
    # "messages" R/T class Project

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
from django.db import models
import re
from datetime import date, datetime

class UserManager(models.Manager):
    def register_validator(self, postData):

        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        # First Name Validation
        first_name = postData.get('first_name', '').strip()
        if len(first_name) < 2:
            errors['first_name'] = "First name must be at least 2 characters long."
        elif not first_name.isalpha():
            errors['first_name'] = "First name must contain letters only."
            
        # Last Name Validation
        last_name = postData.get('last_name', '').strip()
        if len(last_name) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long."
        elif not last_name.isalpha():
            errors['last_name'] = "Last name must contain letters only."

        # Email Validation (Format + Uniqueness Check)
        email = postData.get('email', '').strip()
        if not EMAIL_REGEX.match(email):
            errors['email'] = "Invalid email address format."
        elif self.filter(email=email).exists():
            errors['email'] = "This email is already registered."

        # Birthday Validation
        birthday_str = postData.get('birthday', '').strip()
        if birthday_str:
            try:
                birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                if birthday >= date.today():
                    errors['birthday'] = "Birthday must be a date in the past."
            except ValueError:
                errors['birthday'] = "Invalid date format for birthday. Use YYYY-MM-DD."

        # Password Validation
        password = postData.get('password', '')
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        elif password != postData.get('confirm_password'):
            errors['password'] = "Passwords do not match."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    birthday = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} : {self.email}"

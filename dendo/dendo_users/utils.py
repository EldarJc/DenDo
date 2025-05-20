import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.contrib.auth import login
from django.core.exceptions import ValidationError

from dendo.settings import BASE_DIR
from .models import CustomUser

class UserHelper:    
    @staticmethod
    def get_user(value):
        return CustomUser.objects.filter(Q(email=value) | Q(username=value)).first()

    @staticmethod
    def login_user(request, username_or_email, password):
        user = UserHelper.get_user(username_or_email)

        if user and user.check_password(password):
            login(request, user)
            return user
        
        return None

    @staticmethod
    def create_user(request, username, email, password):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-z]{2,}$', username.strip()):
            raise ValidationError("Username cannot be an email address.")

        elif UserHelper.get_user(username.strip()):
            raise ValidationError("That username is already taken.")

        elif UserHelper.get_user(email.strip().lower()):
            raise ValidationError("Email is already in use.")

        elif not re.match(r"^.{8,}$", password):
            raise ValidationError("Password must be at least 8 characters long")

        new_user = CustomUser.objects.create_user(
            username=username.strip(),
            email=email.strip().lower(),
            password=password
        )

        return UserHelper.login_user(request, username, password)
    
    @staticmethod
    def update_password(user, new_password):
        current_user = user

        if current_user and new_password:
            current_user.set_password(new_password)
            current_user.save()
            return current_user
        
        return None

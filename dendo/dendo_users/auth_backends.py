from django.contrib.auth.backends import ModelBackend

from .utils import UserHelper

class UsernameOrEmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = UserHelper.get_user(username)
            if user and user.check_password(password):
                return user
            return None
        except Exception as e:
            return None
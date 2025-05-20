from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class CustomUser(AbstractUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_avatar = self.avatar
        self._current_banner = self.banner

    first_name=None
    last_name=None

    avatar = models.ImageField( upload_to= 'user_images/', null=True, blank=True)
    banner = models.ImageField( upload_to= 'user_images/', null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.CharField(max_length=160, default='No bio yet.')
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    class Meta:
        db_table = 'CustomUsers'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f'Email: {self.email} Username: {self.username} Created at: {self.date_joined} Updated at: {self.updated_at}'

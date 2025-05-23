from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import CustomUser

@receiver(post_delete, sender=CustomUser)
def remove_images(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete(save=False)
    if instance.banner:
        instance.banner.delete(save=False)
import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import GameAccountImage, GameAccount


@receiver(pre_save, sender=GameAccountImage)
def delete_old_game_account_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(pre_save, sender=GameAccount)
def delete_old_game_account_thumbnail_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_thumbnail = old_instance.thumbnail
    new_thumbnail = instance.thumbnail

    if old_thumbnail and old_thumbnail != new_thumbnail:
        if os.path.isfile(old_thumbnail.path):
            os.remove(old_thumbnail.path)


@receiver(post_delete, sender=GameAccountImage)
def delete_game_account_image_on_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=GameAccount)
def delete_game_account_thumbnail_on_delete(sender, instance, **kwargs):
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)

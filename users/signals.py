from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Followers
from blog.models import Notification


# сигнал для создания нотификации если подписались
@receiver(post_save, sender=Followers)
def create_notification_by_like_post(sender, instance, created, **kwargs):
    if created:
        text = f"Пользователь {instance.owner.username} подписался на '{instance.follow_by.username}'"
        Notification.objects.create(
            owner=instance.owner,
            text=text,
            is_new=True,
            is_prived=False,
            date=timezone.now(),
            initializer=instance.follow_by,
        )


        text = f"Пользователь {instance.owner.username} подписался на '{instance.follow_by.username}'"
        Notification.objects.create(
            owner=instance.follow_by,
            text=text,
            is_new=True,
            is_prived=False,
            date=timezone.now(),
            initializer=instance.owner,
        )

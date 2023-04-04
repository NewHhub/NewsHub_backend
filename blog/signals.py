from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Notification, Like, Reviews_like, Reviews

# сигнал для создания нотификации если лайкнули пост
@receiver(post_save, sender=Like)
def create_notification_by_like_post(sender, instance, created, **kwargs):
    if created:
        if instance.post.owner == instance.user:
            text = f"Вам понравился Ваш пост '{instance.post.title}'"
        else:
            text = f"Пользователю {instance.user.username} понравился ваш пост '{instance.post.title}'"
        Notification.objects.create(
            owner=instance.post.owner,
            text=text,
            is_new=True,
            is_prived=True,
            date=timezone.now(),
            post=instance.post,
            initializer=instance.user,
        )


@receiver(post_save, sender=Reviews)
def create_notification_by_review_like(sender, instance, created, **kwargs):
    if created:
        # действие для владельца поста
        text = f"Пользователь {instance.owner.username} прокоментировал Ваш пост '{instance.post.title}'"
        Notification.objects.create(
            owner=instance.post.owner,
            text=text,
            is_new=True,
            is_prived=False,
            date=timezone.now(),
            post=instance.post,
            initializer=instance.owner,
            review = instance,
        )

        # действие для создателя комента
        text = f"{instance.owner.username} прокоментировал пост '{instance.post.title}'"
        Notification.objects.create(
            owner=instance.owner,
            text=text,
            is_new=True,
            is_prived=False,
            date=timezone.now(),
            post=instance.post,
            initializer=instance.owner,
            review = instance,
        )


@receiver(post_save, sender=Reviews_like)
def create_notification_by_review_like(sender, instance, created, **kwargs):
    if created:
        if instance.review.owner == instance.user:
            text = f"Вы лайкнули свой коментарий '{instance.review.text}' к посту '{instance.review.post}'"
        else:
            text = f"Пользователь {instance.user.username} лайкнул ваш коментарий '{instance.review.text}' к посту '{instance.review.post}'"
        Notification.objects.create(
            owner=instance.review.owner,
            text=text,
            is_new=True,
            is_prived=True,
            date=timezone.now(),
            post=instance.review.post,
            initializer=instance.user,
            review = instance.review,
        )
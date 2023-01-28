from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    bio = models.TextField(_("bio"), max_length=500, blank=True)

class Followers(models.Model):
    owner = models.ForeignKey(User, related_name='following', verbose_name="Владелец", on_delete=models.CASCADE)
    follow_by = models.ForeignKey(User, related_name='followers', verbose_name="Подписан на", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата подписки", blank=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return f'{self.id}_{self.owner}-{self.follow_by}'
from django.db import models
from users.models import User
from django.utils import timezone


class Tags(models.Model):
    text = models.CharField('Текст', max_length=100)
    
    def __str__(self):
        return f'{self.id}_{self.text}'
    

class Post(models.Model):
    title = models.CharField('Название', max_length=300)
    text = models.TextField('Текст поста', blank=True, null=True)
    poster = models.ImageField("Постер", upload_to="blog/", blank=True, null=True)
    draft = models.BooleanField("Черновик", default=False)
    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания", blank=True)
    tag = models.ManyToManyField(Tags, verbose_name='теги', related_name='tag_post')
    
    def __str__(self):
        return f'{self.title}'

    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_by')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_by_likes')
    created = models.DateTimeField(auto_now_add=True)


class Reviews(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', related_name='parent_reviews', verbose_name='Родитель', on_delete=models.CASCADE, blank=True, null=True)
    tread = models.ForeignKey('self', related_name='tread_reviews', verbose_name='Тред', on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, related_name='post_by_review')
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания", blank=True)

    def __str__(self):
        return f"{self.owner} - {self.post} - {self.id}"
    

class Reviews_like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_liker')
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE, related_name='review_for_likes')
    created = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('lp', 'Post Like'),
        ('f', 'Following'),
        ('rc', 'Review Creation'),
        ('rl', 'Review Like'),
        ('no', 'None')
    ]

    owner = models.ForeignKey(User, related_name='notification_owner', verbose_name="Владелец", on_delete=models.CASCADE)
    text = models.TextField('Текст', max_length=500, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата нотификации", blank=True)
    is_prived = models.BooleanField("Приватная", default=False)
    draft = models.BooleanField("Черновик", default=False)
    is_new = models.BooleanField("Новая", default=True)
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPE_CHOICES, default='lp',)

    review = models.ForeignKey(Reviews, related_name='review_notification', verbose_name="Ревью", on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, related_name='post_notification', verbose_name="Пост", on_delete=models.CASCADE, blank=True, null=True)
    initializer = models.ForeignKey(User, related_name='notification_initializer', verbose_name="Инициализатор", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.owner} - {self.text} - {self.id}"
    

    def mark_as_read(self):
        """
        Пометить уведомление как прочитанное
        """
        self.is_new = False
        self.save()


    def display_notification_type(self):
        return dict(Notification.NOTIFICATION_TYPE_CHOICES)[self.notification_type]


    @classmethod
    def create_notification(cls, owner, text, is_prived=False, review=None, post=None, initializer=None, notification_type='no'):
        """
        Создать новое уведомление
        """
        notification = cls(
            owner=owner,
            text=text,
            is_prived=is_prived,
            draft=False,
            is_new=True,
            date=timezone.now(),
            review=review,
            post=post,
            initializer=initializer,
            notification_type=notification_type
        )
        notification.save()
        return notification
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.conf import settings
import datetime


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_of_birth = models.DateField(blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    # def __str__(self):
    #     return 'Профиль пользователя {}'.format(self.user.username)


class Post(models.Model):
    # STATUS_CHOICES = (
    # ('draft', 'Draft'),
    # ('published', 'Published'),
    # )
    title = models.CharField(max_length=20)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month, self.title, self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Email(models.Model):
    email = models.EmailField("email")
    name = models.CharField("Ваше имя", max_length=20, )
    text = models.CharField("Сообщение", max_length=200)

    def get_absolute_url(self):
        return reverse('blog:email')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {0} on {1}'.format(self.name, self.post)

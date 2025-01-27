from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse 
from django.utils.text import slugify


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED  ='PB', 'Published'

    title = models.CharField(max_length=100)
    content = models.TextField(default='new content')
    slug = models.SlugField(max_length=100,unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def save(self,*args,**kwarqgs):

        if not self.slug:
            self.slug=slugify(self.title)

        super().save(*args,**kwarqgs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detial",args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug,
        ])
    
class Comment(models.Model):

    name = models.CharField(max_length=80)
    body = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'comment by {self.name} on {self.post}'
    

from django.db import models
from datetime import datetime

from django.urls import reverse
from .utils import slug_generator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from accounts.models import UsersDetail
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import EmailValidator
from django.conf import settings
import os


class GetNotification(models.Model):
    user_notify     = models.ForeignKey(UsersDetail, null = True, on_delete = models.CASCADE)
    comment         = models.ForeignKey('Comment', null = True, on_delete = models.CASCADE)
    comment_reply   = models.ForeignKey('CommentReply', null = True, on_delete = models.CASCADE)
    text            = models.CharField(max_length = 200, blank = True, null = True)
    text_url        = models.URLField(blank = True)
    mark_as_read_at = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return f'{self.user_notify.username}'

class UserPostManager(models.Manager):
    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        q = query.split(' ')
        lookup = Q(blog_title__icontains=q[0]) | Q(blog_description__icontains=q[0]) | Q(tag__icontains=q[0])
        qs = self.get_queryset().filter(lookup)
        return qs

class UserPost(models.Model):
    user          = models.ForeignKey(User, blank=True, null=True, on_delete = models.CASCADE)
    author        = models.ForeignKey(UsersDetail, blank=True, null=True, on_delete = models.CASCADE)
    blog_id       = models.PositiveIntegerField(null = True, blank = True)
    blog_title    = models.TextField(max_length = 100)
    slug_name     = models.SlugField(blank = True)
    blog_image    = models.ImageField(upload_to = 'media/blog_image', null = True, blank = True,
                    help_text = "<small class='float-right'>Dimension: 800*800>Image>200*200 </small>")
    image_credit  = models.URLField(blank = True, null = True)
    blog_description = RichTextUploadingField(blank=True, null=True)
    is_published  = models.BooleanField(default=False)
    publish_date  = models.DateTimeField(default=datetime.now)
    total_comment = models.PositiveIntegerField(default=0)
    total_views   = models.PositiveIntegerField(default=0)
    reading_time  = models.PositiveIntegerField(default=1, help_text="<small class='float-right'>in minutes</small>")
    tag           = models.TextField(max_length=30, null=True, blank=True, help_text="<small class='float-right'> max length 30</small>")
    category      = models.CharField(max_length=50, null=True, blank=True)
    post_link     = models.URLField(blank=True, null=True)
    fb_id         = models.CharField(max_length=90, null=True, blank=True)

    objects = UserPostManager()

    def publish(self):
        if self.is_published:
            self.is_published = False
        else:
            self.is_published = True
        return self.save()

    def fb_post_id(self, id):
        self.fb_id = id
        return self.save()

    def delete(self, *args, **kwargs):
        from_desc = self.blog_description
        abs_path = getattr(settings, 'MEDIA_ROOT')
        for _ in range(self.blog_description.count('<img')):
            from_desc = from_desc.partition('src="/media/')
            im_path = from_desc[2].partition('.jpg')[0] + '.jpg'
            im_path_thumb = from_desc[2].partition('.jpg')[0] + '_thumb.jpg'
            from_desc = from_desc[2]
            try:
                os.remove(abs_path + im_path)
                os.remove(abs_path + im_path_thumb)
            except:
                pass
        self.blog_image.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f'{self.blog_id} blog_title:- {self.blog_title}'


def post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.post_link and not instance.blog_id:
        instance.blog_id = '110' + str(instance.id) + '12' + str(instance.id)
        instance.post_link = f'http://127.0.0.1:8000/{instance.user.username}/detail/{instance.slug_name}/'
        instance.save()

def pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug_name:
        instance.slug_name = slug_generator(instance)

post_save.connect(post_save_receiver, sender=UserPost)
pre_save.connect(pre_save_receiver, sender=UserPost)


class Comment(models.Model):
    post         = models.ForeignKey(UserPost, on_delete = models.CASCADE, blank=True, null=True)
    email        = models.EmailField(blank = True, null=True,validators = [EmailValidator])
    user         = models.ForeignKey(UsersDetail, on_delete = models.CASCADE, blank=True, null=True)
    like_by      = models.ManyToManyField(UsersDetail, blank=True, related_name='comment_like_by')
    total_likes  = models.PositiveIntegerField(default=0)
    text         = models.TextField()
    date_created = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return f'{self.email}'


class CommentReply(models.Model):
    comment        = models.ForeignKey(Comment, on_delete = models.CASCADE, blank=True, null=True) # manytomanyfield instead of foreignkey
    user_post      = models.ForeignKey(UserPost, on_delete = models.CASCADE, blank=True, null=True)
    email          = models.EmailField(blank = True, null = True, validators = [EmailValidator])
    user           = models.ForeignKey(UsersDetail, on_delete = models.CASCADE, blank=True, null=True)
    like_by        = models.ManyToManyField(UsersDetail, blank=True, related_name='comment_reply_like_by')
    total_r_likes  = models.PositiveIntegerField(default=0)
    reply_to     = models.ForeignKey(UsersDetail, on_delete = models.CASCADE, related_name = 'reply_to_user', blank=True, null=True)
    text         = models.TextField()
    date_created = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return f'{self.email}'

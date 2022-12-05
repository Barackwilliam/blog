import os
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from accounts.models import UsersDetail
from .utils import slug_generator
# Create your models here.

class QuestionAsked(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    slug_name = models.CharField(max_length=255, blank=True, null=True)
    qes_asked_by = models.ForeignKey(User, blank=True, null=True, related_name='qes_by_user', on_delete=models.SET_NULL)
    qes = RichTextUploadingField(blank=True, null=True, config_name='special')
    tag = models.CharField(max_length=255, blank=True, null=True)
    # discussion = models.ForeignKey('Discussion', null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id)

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug_name:
        instance.slug_name = slug_generator(instance)

pre_save.connect(pre_save_receiver, sender=QuestionAsked)

class AnswerBy(models.Model):
    q_asked = models.ForeignKey('QuestionAsked', blank=True, null=True, on_delete=models.CASCADE)
    ans_given_by = models.ManyToManyField(UsersDetail, blank=True, related_name='ans_by_user')
    ans = RichTextUploadingField(blank=True, null=True, config_name='special')
    selected_ans = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now)

    def delete(self, *args, **kwargs):
        from_desc = self.ans
        abs_path = getattr(settings,'MEDIA_ROOT')
        for _ in range(self.ans.count('href')):
            from_desc = from_desc.partition('href="/media/')
            im_path = from_desc[2].partition('.jpg')[0] + '.jpg'
            im_path_thumb = from_desc[2].partition('.jpg')[0] + '_thumb.jpg'
            from_desc = from_desc[2]
            try:
                os.remove(abs_path + im_path)
                os.remove(abs_path + im_path_thumb)
            except:
                pass
        super().delete(*args,**kwargs)

    def __str__(self):
        return str(self.id)


class Discussion(models.Model):
    a_given      = models.ForeignKey('AnswerBy', blank=True, null=True, on_delete=models.CASCADE)
    q_asked      = models.ForeignKey('QuestionAsked', blank=True, null=True, on_delete=models.CASCADE)
    email        = models.EmailField(blank = True, null=True, validators = [EmailValidator])
    user         = models.ForeignKey(UsersDetail, on_delete = models.CASCADE, blank=True, null=True)
    dis_like_by  = models.ManyToManyField(UsersDetail, blank=True, related_name='discussion_like_by')
    total_likes  = models.PositiveIntegerField(default=0)
    text         = models.TextField()
    date_created = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return f'{self.email}'


class DiscussionReply(models.Model):
    discuss        = models.ForeignKey(Discussion, on_delete = models.CASCADE, blank=True, null=True) # manytomanyfield instead of foreignkey
    email          = models.EmailField(blank = True, null = True, validators = [EmailValidator])
    user           = models.ForeignKey(UsersDetail, on_delete = models.CASCADE, blank=True, null=True)
    dis_like_by    = models.ManyToManyField(UsersDetail, blank=True, related_name='discussion_reply_like_by')
    total_likes    = models.PositiveIntegerField(default=0)
    dis_reply_to   = models.ForeignKey(UsersDetail, on_delete = models.CASCADE, related_name = 'dis_reply_to_user', blank=True, null=True)
    text           = models.TextField()
    date_created   = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return f'{self.email}'
import re
from django.db import models
from django.urls import reverse
# from imagekit.models import ImageSpecField,ProcessedImageField
# from imagekit.processors import ResizeToFill
from django.db.models.signals import post_delete
from ckeditor_uploader.fields import RichTextUploadingField
from django.dispatch import receiver
from datetime import datetime
# from blog.models import Comment as discuss
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

# Create your models here.

def check_uname(value):
    if not re.match('^[.a-zA-Z0-9_]+$', str(value)):
        raise ValidationError(f"Invalid Username: '{value}'")


class UsersDetail(models.Model):
    First_name    = models.CharField(max_length=30, blank=True, null=True)
    Last_name     = models.CharField(max_length=30, blank=True, null=True)
    username      = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE,
                                        help_text='<small class="disabled">Must be an unique <strong>Username</strong></small>')
    user_email    = models.EmailField(blank=True, null=True, unique=True, max_length=30, validators=[EmailValidator])
    interests     = models.CharField(max_length=200, blank=True, null=True, help_text='<small class="disabled float-right">max char 200</small>')
    about         = models.TextField(max_length=1000, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='media/author_profile', blank=True, null=True)
    thought       = models.CharField(max_length=100, blank=True, null=True, help_text="<small class='float-right'>max length 100</small>")
    youtube_url   = models.URLField(max_length=200, blank=True, null=True, help_text='<small class="float-right">max char 200</small>')
    facebook_url  = models.URLField(max_length=200, blank=True, null=True, help_text='<small class="float-right">max char 200</small>')
    github_url    = models.URLField(max_length=200, blank=True, null=True, help_text='<small class="float-right">max char 200</small>')
    linkedin_url  = models.URLField(max_length=200, blank=True, null=True, help_text='<small class="float-right">max char 200</small>')
    followers     = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='follow_to')
    notification_as_read = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"-> {self.user_email}"

    def ntf_upd(self, *args, **kwargs):
        self.notification_as_read = datetime.now()
        self.save()
    
    # def get_absolute_url(self):
    #     return reverse("dashboard", kwargs={"slug":self.username.username})

@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for image in sender._meta.concrete_fields:
        if isinstance(image, models.ImageField):
            instance_image_field = getattr(instance, image.name)
            delete_image_if_unused(sender, instance, image, instance_image_field)

def delete_image_if_unused(model, instance, image, instance_image_field):
    dynamic_field = {}
    dynamic_field[image.name] = instance_image_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_image_field.delete(False)

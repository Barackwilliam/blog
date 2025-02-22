# Generated by Django 5.1.5 on 2025-01-23 18:06

import ckeditor_uploader.fields
import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator])),
                ('total_likes', models.PositiveIntegerField(default=0)),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('like_by', models.ManyToManyField(blank=True, related_name='comment_like_by', to='accounts.usersdetail')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.usersdetail')),
            ],
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator])),
                ('total_r_likes', models.PositiveIntegerField(default=0)),
                ('text', models.TextField()),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
                ('like_by', models.ManyToManyField(blank=True, related_name='comment_reply_like_by', to='accounts.usersdetail')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_to_user', to='accounts.usersdetail')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.usersdetail')),
            ],
        ),
        migrations.CreateModel(
            name='GetNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=200, null=True)),
                ('text_url', models.URLField(blank=True)),
                ('mark_as_read_at', models.DateTimeField(default=datetime.datetime.now)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
                ('comment_reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.commentreply')),
                ('user_notify', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.usersdetail')),
            ],
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_id', models.PositiveIntegerField(blank=True, null=True)),
                ('blog_title', models.TextField(max_length=100)),
                ('slug_name', models.SlugField(blank=True)),
                ('blog_image', models.ImageField(blank=True, help_text="<small class='float-right'>Dimension: 800*800>Image>200*200 </small>", null=True, upload_to='media/blog_image')),
                ('image_credit', models.URLField(blank=True, null=True)),
                ('blog_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('publish_date', models.DateTimeField(default=datetime.datetime.now)),
                ('total_comment', models.PositiveIntegerField(default=0)),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('reading_time', models.PositiveIntegerField(default=1, help_text="<small class='float-right'>in minutes</small>")),
                ('tag', models.TextField(blank=True, help_text="<small class='float-right'> max length 30</small>", max_length=30, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('post_link', models.URLField(blank=True, null=True)),
                ('fb_id', models.CharField(blank=True, max_length=90, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.usersdetail')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commentreply',
            name='user_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.userpost'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.userpost'),
        ),
    ]

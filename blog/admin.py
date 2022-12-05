from django.contrib import admin
from .models import UserPost,Comment,CommentReply,GetNotification

admin.site.register(UserPost)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(GetNotification)

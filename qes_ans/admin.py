from django.contrib import admin
from .models import QuestionAsked, AnswerBy, Discussion, DiscussionReply
# Register your models here.
admin.site.register(QuestionAsked)
admin.site.register(AnswerBy)
admin.site.register(Discussion)
admin.site.register(DiscussionReply)
from django.urls import re_path, path, include
from django.contrib.auth.decorators import login_required
from . import views
from ckeditor_uploader import views as editor_views

urlpatterns = [
    path('upload/', login_required(editor_views.upload), name='ckeditor_upload'),
    path('browse/', login_required(editor_views.browse), name='ckeditor_browse'),
    path('q_and_a/', views.question_asked, name='q_and_a'),
    path('answer/', views.answer_given, name='answer'),
    path('<slug:discussion_type>/discuss_q_and_a/', views.discuss_q_and_a, name='discuss_q_and_a'),
    re_path(r'^(?P<id>[\w-]+)/', include([
        path('edit/question/', views.edit_question, name='edit_question'),
        path('edit/ans/', views.edit_answer, name='edit_answer'),
        path('<int:q_id>/selected_ans/', views.select_answer, name='select_answer'),
        path('delete/answer/', views.delete_answer, name='delete_answer'),
        path('delete/question/', views.delete_question, name='delete_question'),
        path('<slug:dis_from>/discussion/', views.get_qes_discussion, name='get_discussion'),
        path('<slug:q_title>/answer/', views.all_answers, name='all_answer'),
        path('like_unlike/<slug:dis_type>/', views.discussion_like_unlike, name='discussion_like_unlike'),
        path('<slug:discussion_type>/', include([
            path('edit/discussion/', views.discuss_edit, name='discuss_edit'),
            path('delete/discussion/', views.discuss_delete, name='discuss_delete'),
        ])),
    ])),
    # path('<int:id>/edit/question/', views.edit_question, name='edit_question'),
    # path('<int:id>/edit/ans/', views.edit_answer, name='edit_answer'),
    # path('<int:id>/<int:q_id>/selected_ans/', views.select_answer, name='select_answer'),
    # path('<int:id>/delete/question/', views.delete_question, name='delete_question'),
    # path('<int:id>/like_unlike/<slug:dis_type>/', views.discussion_like_unlike, name='discussion_like_unlike'),
    # re_path(r'^(?P<id>[\w-]+)/(?P<dis_from>[\w-]+)/discussion/', views.get_qes_discussion, name='get_discussion'),
    # path('<int:id>/<slug:q_title>/answer/', views.all_answers, name='all_answer'),
    # re_path(r'^(?P<id>[\w-]+)/(?P<discussion_type>[\w-]+)/edit/discussion/', views.discuss_edit, name='discuss_edit'),
    # re_path(r'^(?P<id>[\w-]+)/(?P<discussion_type>[\w-]+)/delete/discussion/', views.discuss_delete, name='discuss_delete'),
]
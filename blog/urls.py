from django.urls import include,path,re_path
from . import views as main_views
from django.contrib.auth.decorators import login_required
from ckeditor_uploader import views


urlpatterns = [
    re_path(r'^all_activity/$', main_views.UserActivity.as_view(), name='all_activity'),
    re_path(r'^$', main_views.PageListView.as_view(), name='page_list'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^(?P<slu>[\w.-]+)/detail/(?P<slug>[\w.-]+)/$', main_views.DetailPageView.as_view(), name = 'detail_page'),
    re_path(r'^(?P<slu>[\w.-]+)/delete/(?P<slug>[\w.-]+)/$', main_views.delete_post,name='delete'),
    re_path(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
    re_path(r'^browse/', login_required(main_views.ck_editor), name='ckeditor_browse'),
    re_path(r'^(?P<slug>[\w.-]+)/follow_to/', main_views.following, name='follow_to'),
    re_path(r'^(?P<slu>[\w.-]+)/post_blog/', main_views.user_post_form, name='post_blog'),
    re_path(r'^(?P<slu>[\w.-]+)/(?P<id>[\w.-]+)/edit/', main_views.user_post_edit, name='post_edit'),
    re_path(r'^(?P<slu>[\w.-]+)/(?P<id>[\w.-]+)/post/', main_views.publish_post, name='update'),
    # re_path(r'^(?P<slu>[\w.-]+)/detail/(?P<slug>[\w.-]+)/$', main_views.detail_page, name='detail_page'),
    re_path(r'^(?P<slug>[\w.-]+)/notifications/', main_views.hide_notification, name='hide_notification'),
    re_path(r'^(?P<comment_type>[\w-]+)/(?P<id>[\w-]+)/toggle_like/', main_views.comment_likes, name='comment_likes'),
    re_path(r'^(?P<slu>[\w.-]+)/comment/', main_views.public_comment, name='public_comment'),
    re_path(r'^(?P<comment_type>[\w-]+)/(?P<id>[\w-]+)/edit_comment/', main_views.edit_public_comment, name='edit_comment'),
    re_path(r'^(?P<comment_type>[\w-]+)/(?P<id>[\w-]+)/comment_delete/', main_views.comment_delete, name='comment_delete'),
    re_path(r'^notification/$', main_views.UserNotification.as_view(), name='user_notification'),
    re_path(r'^search/$', main_views.search_engine, name='search_engine'),
    re_path(r'^get_comment/(?P<id>[\w-]+)/$', main_views.get_comment, name='get_comment'),
    re_path(r'^get_notification/$', main_views.all_notification_new, name='all_notification'),
    path('practice/',main_views.practice, name='practice')

    ]

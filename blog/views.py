from cgitb import lookup
from django.shortcuts import render, redirect, get_object_or_404, Http404
from itertools import chain
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.html import escape
from django.template import loader
from django.template.defaultfilters import urlize
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Prefetch, Count, Subquery, OuterRef
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from blog.forms import PostEditForm, PostForm
from blog.user_notification import update_notification
from qes_ans.models import QuestionAsked
from accounts.forms import PopUpForm
import facebook
from django.contrib import messages, auth
from django.contrib.auth.models import User
from accounts.models import UsersDetail
from blog.models import UserPost, Comment, CommentReply, GetNotification
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms import ValidationError
# from IPython.display import display_html
from ckeditor_uploader import views as ck_views

# Create your views here.


def practice(request):
    usr_dtl = UsersDetail.objects.select_related().filter(user_email=request.user.email)
    return render(request, 'partials/practice.html',{'usr_dtl':usr_dtl})

def following(request, slug=None, id=None):
    auth_user = None
    user = User.objects.filter(username=slug).first()
    if request.user.is_authenticated:
        auth_user = UsersDetail.objects.filter(username=request.user).first()
    prefetch = Prefetch('follow_to', queryset=UsersDetail.objects.prefetch_related('followers').select_related('username'), to_attr='folwer')
    following = UsersDetail.objects.filter(user_email=user.email).prefetch_related(prefetch).first()
    if following:
        p = Paginator(following.folwer, 20)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
        username = request.user
        user_authenticated = username.is_authenticated
        context = {
            'auth_user':auth_user,
            'pop_form':PopUpForm(),
            'req_username': str(username),
            'username': str(username),
            'user_authenticated': user_authenticated,
            'following':following,
            'follow_to':page_obj
        }

        return render(request, 'partials/following.html', context)
    else:
        return redirect('login')


def ck_editor(request):
    try:
        ck_views.browse
    except:
        return redirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required
def comment_delete(request, id=None, comment_type=None):
    if id and comment_type == 'reply_comment':
        get_comment = CommentReply.objects.filter(id=id).select_related('user_post').prefetch_related('getnotification_set').first()
        if get_comment.user.user_email == str(request.user.email) or get_comment.user_post.user.user_email == request.user.email:
            get_comment.user_post.total_comment = F('total_comment') - 1
            get_comment.user_post.save()
            get_comment.getnotification_set.all().delete()
            get_comment.delete()
            text = 'This content is no longer exist.'
            return JsonResponse({'success': True, 'text': text}, status=200)
        else:
            return JsonResponse({'success': False}, status=400)

    elif id and comment_type == 'main_comment':
        get_comment = Comment.objects.filter(id=id).select_related('post').prefetch_related('getnotification_set').first()
        if get_comment.user.user_email == str(request.user.email) or get_comment.post.author.user_email == request.user.email:
            get_comment.post.total_comment = F('total_comment') - 1
            get_comment.post.save()
            get_comment.getnotification_set.all().delete()
            get_comment.commentreply_set.all().delete()
            get_comment.delete()
            text = 'This content is no longer exist.'
            return JsonResponse({'success': True, 'text': text}, status=200)
        else:
            return JsonResponse({'success': False}, status=400)
    else:
        return JsonResponse({'success': False}, status=400)



@login_required
def comment_likes(request, id=None, comment_type=None):
    if request.method == 'POST':
        user_detail = UsersDetail.objects.filter(
            user_email=request.user.email).first()
        if comment_type == 'reply_comment':
            get_comment = get_object_or_404(CommentReply, id=id)
            return go_inside(request, get_comment, user_detail)
        elif comment_type == 'main_comment':
            get_comment = get_object_or_404(Comment, id=id)
            return go_inside(request, get_comment, user_detail)
    else:
        return JsonResponse({'path': str(request.path)}, status=400)


def go_inside(request, get_comment=None, user_detail=None):
    if user_detail == get_comment.like_by.filter(user_email=request.user.email).first():
        get_comment.like_by.remove(user_detail)
        condition = 'like'
    else:
        get_comment.like_by.add(user_detail)
        condition = 'unlike'

    data = {'condition': condition,
            'count': get_comment.like_by.count()
        }

    return JsonResponse(data, status=200)

def date_frequency():
    timelimit = datetime.now() - timedelta(days=365)
    pass

def all_notification_new(request):
    if request.user.is_authenticated:
        context = {}
        prefetch = Prefetch('getnotification_set', queryset=GetNotification.objects.all())
        nav_user = UsersDetail.objects.prefetch_related(prefetch, 'username').filter(user_email=request.user.email).first()
        tm = nav_user.notification_as_read
        notification = nav_user.getnotification_set.filter(
            Q(mark_as_read_at__lte=datetime.now())).order_by('-mark_as_read_at').values('text','text_url')
        notification_count = notification.filter(
            Q(mark_as_read_at__gte=tm)).count()
        if nav_user.profile_photo:
            context.update({'profile_photo':nav_user.profile_photo.url})
        else:
            context.update({'profile_photo':'/static/assets/img/17004.svg'})
        context.update({
            'nav_username':nav_user.username.username,
            'total_notification_count': notification.count(),
            'notification': list(notification),
            'unread_notification': notification_count
        })
        return JsonResponse(context, status=200)
    pass 


class DetailPageView(DetailView):
    template_name = 'blog/detail.html'

    def get_queryset(self, *args, **kwargs):
        follower_count = self.object.author.followers.count()
        return follower_count

    def get_object(self, *args, **kwargs):
        request = self.request
        try:
            '''
                fetch the particular userpost from database and also fetch their user using select_related
                so that we can show the userpost with usersdetail
            '''
            obj = get_object_or_404(UserPost.objects.select_related('author__username').annotate(follower_count=Count('author__followers')), slug_name=self.kwargs['slug'])
            blog_view = request.session.get('blog_view', None)
            if not request.user.is_authenticated and blog_view is None:
                request.session['blog_view'] = obj.blog_title
                obj.total_views = F('total_views') + 1
                obj.save()
                obj.refresh_from_db()

        except UnboundLocalError:
            messages.error(request, 'wrong url provided')
            return redirect('/')
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(DetailPageView, self).get_context_data(*args, **kwargs)
        obj = self.object
        request = self.request
        username = request.user
        author = obj.author
        author_username = author.username.username
        author_id = author.id
        user_authenticated = username.is_authenticated
        qs = QuestionAsked.objects.filter(qes_asked_by=User.objects.filter(username=author_username).first()).select_related('qes_asked_by')
        if str(username) == str(author_username) and not obj.is_published:
            '''Check if authenticated user is the owner of this particular post?? if not, then check post is
                publised by the owner
            '''
            context.update({
                'question':qs,
                'req_username': str(username),
                'username': str(username),
                'user_authenticated': user_authenticated,
                'userpost': obj,
                'useracc': author,
                'author_username': author_username,
                'author_id': author_id,
                'path': request.path
            })
            return context
        elif not user_authenticated and not obj.is_published:
            obj = False
        if obj:
            obj_tag1 = obj.tag.split(',')
            tag_post = UserPost.objects.filter(Q(tag__icontains=obj_tag1[0]) | Q(tag__icontains=obj_tag1[1]), is_published=True).select_related(\
                'author').exclude(slug_name=self.kwargs['slug']).order_by('-publish_date')[0:6]
            
            rel_question = QuestionAsked.objects.filter(Q(tag__icontains=obj_tag1[0]) | Q(tag__icontains=obj_tag1[1])).select_related()[:8]
            p_register = PopUpForm()
            if user_authenticated:
                nav_user = UsersDetail.objects.filter(username=username).select_related(
                    'username').first()
                context.update({'nav_bar_user':nav_user})
            context.update({
                'question':qs,
                'rel_question':rel_question,
                'tag_post': tag_post,
                'req_username': str(username),
                'user_authenticated': user_authenticated,
                'username': str(username),
                'userpost': obj,
                'useracc': author,
                'author_username': author_username,
                'author_id': author_id,
                'path': request.path,
                'pop_form': p_register
            })
        else:
            raise Http404('Wrong url provided')

        return context


@login_required
def delete_post(request, slug=None, slu=None):
    item = UserPost.objects.filter(slug_name=slug).select_related('author').first()
    if request.user == item.author.username:
        if item:
            fb(item, delete_post=12)
            item.delete()
            messages.success(
                request, 'Your blog {0} had deleted'.format(item.blog_title))
            return redirect('/account/{0}/dashboard/'.format(item.author.username))

        else:
            messages.error(request, 'Sorry, something went wrong.')
            return redirect('/account/{0}/dashboard/'.format(item.author.username))

    else:
        messages.error(request, 'Sorry, you have not permission.')
        return HttpResponseRedirect(reverse('detail_page', args=[str(item.author.username), slug], current_app='blog'))


@login_required
def edit_public_comment(request, comment_type, id):
    message = urlize(escape(request.POST.get('message', None)))
    if id and comment_type == 'reply_comment' and message:
        get_comment = get_object_or_404(CommentReply, id=id)
        username = get_comment.email.split('@')[0]
        if username == str(request.user.username):
            get_comment.text = message
            get_comment.save()
            return JsonResponse({'success': True, 'text': message}, status=200)
        else:
            return JsonResponse({'success': False}, status=400)

    elif id and comment_type == 'main_comment' and message:
        get_comment = get_object_or_404(Comment, id=id)
        username = get_comment.email.split('@')[0]
        if username == str(request.user.username):
            get_comment.text = message
            get_comment.save()
            return JsonResponse({'success': True, 'text': message}, status=200)
        else:
            return JsonResponse({'success': False}, status=400) 
    else:
        return redirect('/')


def fb(post, delete_post=None):
    token = {
        'page_id': '109522220665652',
        'fb_page_token': 'EAAYuePgNJbMBANMYZAPUc4W582ZBORtACasCBjkEFNTMIfsRJ2EL8aFHlUAeZCQRhG2AojZB2YTDvZAaqnJKqRM4OR1v90MCZCWmEV6qM9488f9MCgqlAn9qEZCIgWSRxSDhjMf0bDBxiZBPhroiFc1n5B7VXZAYaQZCUA8yE89L3vaPKcg7ZBRy5btK0xBuPJBXFoZD'
    }
    if delete_post:
        try:
            api = facebook.GraphAPI(token['fb_page_token'])
            api.delete_object(post.fb_id)
        except:
            pass
    else:
        img_path = post.blog_image.path
        title = post.blog_title
        try:
            user_name = post.author.First_name + ' ' + post.author.Last_name
        except:
            user_name = post.user.username
        path = f'Uploaded by: {user_name} \n' + \
            f'Blog Name: {title}\n ' + f'See more: {post.post_link}'
        try:
            api = facebook.GraphAPI(token['fb_page_token'])
            x = api.put_photo(open(img_path, 'rb'), parent_object='me',
                              connection_name='feed', message=path)
            return x['post_id'], post
        except:
            return 'error', post


def get_comment(request, id=None, start=0, end=3):
    usersdetail = UsersDetail.objects.filter(
        username=request.user).only('id').first()
    cr_prefetch = Prefetch('commentreply_set', queryset=CommentReply.objects.select_related(
        'reply_to', 'user').prefetch_related('like_by'), to_attr='commentreply_list')
    comment = Comment.objects.select_related('user').prefetch_related(
        'like_by').prefetch_related(cr_prefetch)
    prefetch = Prefetch('comment_set', queryset=comment,
                        to_attr='comment_list')
    user_post = UserPost.objects.filter(id=id).select_related(
        'user').prefetch_related(prefetch).first()
    data = {
        'req_username': request.user.username,
        'end': end,
        'user_authenticated': request.user.is_authenticated,
        'post_id': id,
        'post_slug_name': user_post.slug_name,
        'post_author_username': str(user_post.user.username),
    }
    n = 0
    for comment in user_post.comment_list:
        c_like = comment.like_by.all()[:]
        c_like_count = len(c_like)
        c_username = comment.email.split('@')[0]
        data['c_count'] = n
        data[f'c_id_{n}'] = comment.id
        data[f'c_username_{n}'] = c_username
        data[f'c_First_name_{n}'] = comment.user.First_name
        data[f'c_Last_name_{n}'] = comment.user.Last_name
        if comment.user.profile_photo:
            data[f'c_profile_photo_{n}'] = comment.user.profile_photo.url
        data[f'c_date_created_{n}'] = str(comment.date_created).split(' ')[0]
        data[f'c_text_{n}'] = comment.text
        if c_like_count > 0 and usersdetail in c_like:
            data[f'c_like_count_{n}'] = str(c_like_count)
            data[f'c_like_unlike_btn_{n}'] = 'unlike'
        elif c_like_count > 0:
            data[f'c_like_count_{n}'] = str(c_like_count)
            data[f'c_like_unlike_btn_{n}'] = 'like'
        else:
            data[f'c_like_count_{n}'] = ''
            data[f'c_like_unlike_btn_{n}'] = 'like'

        z = 0

        for comment_repl in comment.commentreply_list:
            z += 1
            cr_like = comment_repl.like_by.all()[:]
            cr_like_count = len(cr_like)
            # we need to find how many reply-comment of a particular main-comment
            data[f'cr_count_{n}'] = z
            data[f'cr_id_{n}_{z}'] = comment_repl.id
            data[f'cr_username_{n}_{z}'] = comment_repl.email.split('@')[0]
            data[f'cr_First_name_{n}_{z}'] = comment_repl.user.First_name
            data[f'cr_Last_name_{n}_{z}'] = comment_repl.user.Last_name
            if comment_repl.user.profile_photo:
                data[f'cr_profile_photo_{n}_{z}'] = comment_repl.user.profile_photo.url
            data[f'cr_date_created_{n}_{z}'] = str(
                comment_repl.date_created).split(' ')[0]
            data[f'cr_text_{n}_{z}'] = comment_repl.text
            data[f'cr_reply_to_{n}_{z}'] = comment_repl.reply_to.user_email.split(
                '@')[0]
            if cr_like_count > 0 and usersdetail in cr_like:
                data[f'cr_like_count_{n}_{z}'] = str(cr_like_count)
                data[f'cr_like_unlike_btn_{n}_{z}'] = 'unlike'
            elif cr_like_count > 0:
                data[f'cr_like_count_{n}_{z}'] = str(cr_like_count)
                data[f'cr_like_unlike_btn_{n}_{z}'] = 'like'
            else:
                data[f'cr_like_count_{n}_{z}'] = ''
                data[f'cr_like_unlike_btn_{n}_{z}'] = 'like'

        n += 1
    return JsonResponse(data, status=200)


@login_required
def hide_notification(request, slug):
    if request.user.is_authenticated:
        nt_count = UsersDetail.objects.filter(user_email=request.user.email).first()
        nt_count.ntf_upd()
        return JsonResponse({'hide': True}, status=200)
    else:
        return redirect('/')


class PageListView(ListView):
    queryset = UserPost.objects.select_related('user').order_by(
        '-publish_date').filter(is_published=True).annotate(post_num=Count('user', distinct=True))
    paginate_by = 8
    template_name = 'page_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PageListView, self).get_context_data(*args, **kwargs)
        _user = self.request.user
        rel_question = QuestionAsked.objects.all().order_by('-date_created')[:10]
        context['popular_post'] = self.queryset.order_by('-total_views')[0:5]
        if not self.queryset:
            context['object_list'] = []
            context['popular_post'] = []
        context['superuser'] = _user.is_superuser
        context['req_username'] = _user.username
        context['user_authenticated'] = _user.is_authenticated
        context['rel_question'] = rel_question
        return context


def public_comment(request, slu=None):
    if request.user.is_authenticated and request.method == "POST":
        post_id = request.POST.get('post', None)
        reply_to = request.POST.get('reply_to', None)
        text = urlize(escape(request.POST.get('message', None)))
        comment_id = request.POST.get('comment_id', None)
        user = User.objects.filter(username=request.user.username).first()
        usersdetail = user.usersdetail
        reply_to = User.objects.filter(username=reply_to).first()
        post = UserPost.objects.prefetch_related(
            'comment_set').filter(id=post_id).first()
        main_comment = post.comment_set.filter(id=comment_id).first()
        if not usersdetail:
            messages.warning(request, 'Please update your account')
            return JsonResponse({'success': False, 'path': f'/account/social/{user.username}/update/'}, status=400)
        if post and main_comment and text and usersdetail:
            post.total_comment = F('total_comment') + 1
            post.save()
            post.refresh_from_db()
            rep_comment = CommentReply(comment=main_comment, user_post=post, user=usersdetail,
                                       reply_to=reply_to.usersdetail, email=user.email, text=text)
            rep_comment.save()
            update_notification(request, 'public_comment_reply', extra={
                                'rep_user': reply_to, 'post': post, 'div_comment': main_comment}, text=text, id=rep_comment.id)
            return JsonResponse({'success': True}, status=200)
        elif post and text:
            post.total_comment = F('total_comment') + 1
            post.save()
            post.refresh_from_db()
            comment_crt = Comment(
                post=post, user=usersdetail, email=user.email, text=text)
            comment_crt.save()
            update_notification(request, 'public_comment_main', extra={
                                'post': post, 'all_reltd_comment': post.comment_set.all()}, text=text, id=comment_crt.id)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': True}, status=200)
    else:
        return JsonResponse({'success': False, 'path': f'/account/register/'}, status=400)


@login_required
def publish_post(request, id=None, slu=None):
    item = UserPost.objects.filter(id=id).select_related('author').first()
    _ = request.get_full_path()
    if request.user.email == item.author.user_email:
        post_id, post = fb(item)
        update_notification(request, 'publish_post', item)
        item.publish()
        post.fb_post_id(post_id)
        if item.is_published:
            messages.success(request, 'Now, your blog is seen by everyone.')
        else:
            messages.warning(request, 'This blog is hide for other person.')
            return redirect(_)
        return redirect('/account/{0}/dashboard/'.format(slu))
    else:
        messages.error(request, 'Sorry, you have not permission.')
        return redirect('/')


def search_engine(request):
    query = str(request.GET.get('query'))
    filter_query = str(request.GET.get('f', '1'))
    q = query.split(' ')
    page_number = request.GET.get('page')
    lookup = Q(user_email__icontains=q) | Q(First_name__icontains=q[0]) | Q(Last_name__icontains=q[0]) | Q(interests__icontains=q[0])
    UserName = UsersDetail.objects.filter(lookup \
        ).select_related('username').annotate(foll_count=Count('followers', distinct=True),post_count=Count('userpost',distinct=True)).order_by('-foll_count', '-post_count').distinct()
    allUserPost = UserPost.objects.search(query=query).order_by('total_views', 'publish_date')
    
    if filter_query:
        if filter_query == 'username':
            u_name = UserName
            all_post = UserPost.objects.none()
        elif filter_query == 'blog':
            all_post = allUserPost
            u_name = UsersDetail.objects.none()
        else:
            u_name = UserName
            all_post = allUserPost
    else:
        u_name = UserName
        all_post = allUserPost
        
        
        # post = UserPost.objects.filter(Q(tag__search=q) | Q(blog_description__search=q) | Q(blog_title__search=q), is_published=True).select_related(\
        #     'author__username').distinct().order_by('-total_views') # not working with MySQL database
        # question_ask = QuestionAsked.objects.filter(Q(title__search=q) | Q(tag__search=q)).select_related().distinct().order_by('-id')
        # u_name = UsersDetail.objects.filter(First_name__icontains=q).select_related(\
        #         'username').annotate(foll_count=Count('followers', distinct=True), post_count=Count('userpost', \
        #         distinct=True)).order_by('-foll_count', '-post_count').distinct()
        
    question_ask = QuestionAsked.objects.filter(Q(tag__icontains=q[0]) | \
                    Q(title__icontains=q[0])).order_by('-date_created')[:10]
    search_result = list(chain(all_post, u_name))
    # q_paginator = Paginator(question_ask, 10)
    u_paginator = Paginator(search_result, 8)
    # paginator = Paginator(post, 10)
    u_obj = u_paginator.get_page(page_number)
    # page_obj = paginator.get_page(page_number)
    # question_obj = q_paginator.get_page(page_number)
    context = {}
    if request.user.is_authenticated:
        _user = request.user
        context['superuser'] = _user.is_superuser
        context['req_username'] = _user.username
        context['user_authenticated'] = _user.is_authenticated
    context.update({'all_result':u_obj, 'rel_question':question_ask})
    if not search_result:
        context.update({'all_result': None})
        return render(request, 'partials/search.html', context)
    return render(request, 'partials/search.html', context)


class UserNotification(ListView):
    template_name = 'partials/user_notification.html'
    paginate_by = 20
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.ntify = get_object_or_404(UsersDetail.objects.prefetch_related('getnotification_set'), \
                        user_email=self.request.user.email)
            return self.ntify.getnotification_set.order_by('-mark_as_read_at').all()
        return []

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        _user = self.request.user
        if _user.is_authenticated:
            context['superuser'] = _user.is_superuser
            context['req_username'] = _user.username
            context['user_authenticated'] = _user.is_authenticated
            
        return context


class UserActivity(LoginRequiredMixin, ListView):
    template_name = 'partials/all_activity.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            ntify = UsersDetail.objects.filter(user_email=str(
                self.request.user.email)).prefetch_related('userpost_set__author','getnotification_set','comment_set__user','commentreply_set__user')
            return ntify
        return []

    def get_context_data(self, *args, **kwargs):
        context = super(UserActivity, self).get_context_data(*args, **kwargs)

        _user = self.request.user
        page_number = self.request.GET.get('page')
        usersdetail = self.get_queryset().first()
        all_post = usersdetail.userpost_set.order_by('-publish_date')
        post = Paginator(all_post, 2)
        all_post = post.get_page(page_number)
        context['superuser'] = _user.is_superuser
        context['req_username'] = _user.username
        context['user_authenticated'] = _user.is_authenticated
        context['all_post'] = all_post
        context['nav_user'] = usersdetail
        return context


@login_required
def user_post_form(request, slu=None):
    _user, req_username = request.user, request.user.username
    user_authenticated = _user.is_authenticated
    dash_user = UsersDetail.objects.select_related('username').prefetch_related(
        'getnotification_set').filter(user_email=_user.email).first()
    context = {}
    if request.method == 'POST' and dash_user:
        post_form = PostForm(request.POST or None, request.FILES or None)
        # After checking form , again check form is valid or not.
        if post_form.is_valid() and dash_user:
            instance = post_form.save(commit=False)

            instance.user = dash_user.username
            instance.author = dash_user
            instance.save()
            messages.success(request, 'Post saved successfully')
            return redirect(f'/{req_username}/detail/{instance.slug_name}/')
        else:
            context.update({'form': post_form, 'req_username': req_username,
                            'user_authenticated': user_authenticated})
            if ValidationError:
                messages.error(request, 'Please checked below error')
                return render(request, 'blog/post_form.html', context)

            elif KeyError:
                messages.error(request, 'Something went wrong')
                return render(request, 'blog/post_form.html', context)
            else:
                post_form = PostForm()
                messages.error(
                    request, 'We get server error please fill everything again.')
                return render(request, 'blog/post_form.html', context)
            return render(request, 'blog/post_form.html', context)

    elif user_authenticated and dash_user:
        post_form = PostForm()
        context.update({'form': post_form, 'req_username': req_username,
                        'user_authenticated': user_authenticated})
        return render(request, 'blog/post_form.html', context)
    elif user_authenticated and not dash_user:
        return HttpResponseRedirect(f'/account/social/{req_username}/update/')
    else:
        return redirect('/')


@login_required
def user_post_edit(request, id=None, slu=None):
    try:
        get_post = get_object_or_404(UserPost.objects.prefetch_related(
            'author__followers'), pk=id)
    except ValueError:
        return redirect(f'/account/{str(request.user)}/dashboard/')
    if get_post and request.user == get_post.author.username:
        context = {}
        if request.method == 'POST':
            edit_form = PostEditForm(
                request.POST or None, request.FILES or None, instance=get_post)
            category = request.POST.get('category')
        else:
            edit_form = PostEditForm(request.POST or None, instance=get_post)
        if edit_form.is_valid():
            get_post.category = category
            instance = edit_form.save()
            update_notification(request, 'post_edit',
                                extra=get_post, id=get_post.id)
            return redirect(f'/{str(request.user)}/detail/{get_post.slug_name}/')

        context.update({'form': edit_form, 'post': get_post,'req_username': request.user.username,
                        'user_authenticated': request.user.is_authenticated})
        return render(request, 'blog/post_form.html', context)
    else:
        messages.error(request, 'Sorry, this post is not related to you.')
        return redirect('/')

from telnetlib import STATUS
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q, Count, Prefetch
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.views import all_notification_new
# from Blogging.captcha import clean
import json
from django.contrib.auth.models import User
from .models import UsersDetail
from qes_ans.models import QuestionAsked
from blog.user_notification import update_notification
from blog.models import UserPost, Comment, CommentReply, GetNotification
from django.contrib import messages, auth
from django.http import JsonResponse
from .forms import (UsersDetailForm, PopUpForm, UsersUpdateForm,\
                    UsersUpdate2Form, SocialUsersUpdateForm, check_uname)
# Create your views here.

def comments_hover_user(request, slug):
    user = get_user(slug).first()
    if request.user.is_authenticated:
        usrs_dtl = UsersDetail.objects.filter(user_email=user.email).annotate(follower_count=Count('followers')).values()
        usrs_dtl = usrs_dtl[0]
        usrs_dtl.update({'hover_username':slug})
        return JsonResponse(usrs_dtl, status=200)
    return JsonResponse({},status=400)

def check_follow(req_user, dash_user):
    if not dash_user.follower_count:
        dash_user.follower_count = 0
        flo_unflo = 'follow'
        return flo_unflo
    elif dash_user.followers.filter(user_email=req_user.email).exists():
        flo_unflo = 'unfollow'
        return flo_unflo
    else:
        flo_unflo = 'follow'
        return flo_unflo

def restless(request):
    ids = [i for i in range(3, 500)]
    from django.contrib.auth.hashers import make_password
    d = {1:'newthing', 2:'2nd thing'}
    usr = User.objects.in_bulk(ids)
    ls = [usr.get(i) for i in range(3, 451)]
    for i in range(3, 451):
        ls[i-3].password = make_password('aman4321')
    User.objects.bulk_update(ls, ['password'])
    return JsonResponse({1:'hmm'}, status=200)
    # from itertools import islice
    # thought = ['Practice makes man perfect', 'Simple is better than complex', 'Courage is grace under pressure.',\
    #     'Success is walking from failure to failure with no loss of enthusiasm.', "Opportunities don't happen. You create them"]
    # about = "Hi it's me. I loves Science and related tech. Lorem ipsumIt casts objs to a list, which fully evaluates objs if it's\
    #  a generator. The cast allows inspecting all objects so that any objects with a manually set \
    #  primary key can be inserted first. If you want to insert objects in batches without evaluating \
    #     the entire generator at once, you can use this technique as long as the objects dont have any \
    #     manually set primary keys"
    # fname = ['rajesh', 'suresh', 'dinesh', 'mahesh', 'kamlesh', 'preetam', 'aman']
    # lname = ['tripathi', 'sah', 'yadav', 'roy', 'sharma', 'maheswari', 'raj']
    # interset = ['Programing, Science', 'Physics, Python, AI', 'Python, Programming, Science', 'Python, Django']
    # import random
    # usr = ()
    # objs = ()
    # for i in range(500):
    #     f_nam = random.choice(fname)
    #     l_nam = random.choice(lname)
    #     intr = random.choice(interset)
    #     usr += (User(first_name=f'{f_nam}{i}', last_name=l_nam, email=f'{f_nam}{i}@gmail.com', username=f'{f_nam}{i}', password='aman@1234'),)
    #     objs += (UsersDetail(First_name=f'{f_nam}{i}', Last_name=l_nam, username=usr[i], user_email=f'{f_nam}{i}@gmail.com', interests=intr,\
    #         about=about, thought=random.choice(thought) ),)
    # i_usr = list(islice(usr, 450))
    # User.objects.bulk_create(i_usr, batch_size=450, ignore_conflicts=True)
    # u_detail = list(islice(objs, 450))
    # UsersDetail.objects.bulk_create(u_detail, batch_size=450, ignore_conflicts=True)
    


def dashboard(request, slug=None):
    req_user = request.user
    user_authenticated = req_user.is_authenticated
    user = get_user(slug).first()
    qs = QuestionAsked.objects.select_related('qes_asked_by').filter(qes_asked_by=user)
    context = {'question':qs}
    if not user_authenticated:
        prefetch = Prefetch('userpost_set', queryset=UserPost.objects.filter(is_published=True).order_by('-publish_date'), to_attr='user_post')
        follower = Prefetch('followers')
        dash_user = UsersDetail.objects.filter(username=user).prefetch_related(prefetch).prefetch_related(follower).annotate(follower_count=Count('followers')).first()
        post = Paginator(dash_user.user_post, 2)
        page_number = request.GET.get('page')
        page_obj = post.get_page(page_number)
        context.update({
            'dash_user':dash_user,
            'dash_user_username':user,
            'user_post':page_obj,
            'pop_form':PopUpForm(),
            'user_authenticated':user_authenticated,
        })
        return render(request, 'accounts/dashboard.html', context)

    elif user_authenticated and user and not req_user.username == user.username: # Authenticated user see another user dashboard
        prefetch = Prefetch('userpost_set', queryset=UserPost.objects.filter(is_published=True).order_by('-publish_date'), to_attr='user_post')
        follower = Prefetch('followers')
        dash_user = UsersDetail.objects.select_related('username').prefetch_related(prefetch).prefetch_related(follower).annotate(follower_count=Count('followers',distinct=True)).filter(user_email=user.email).first() # dashboard and their post
        post = Paginator(dash_user.userpost_set.all().filter(is_published=True).order_by('-publish_date'), 10)
        page_number = request.GET.get('page')
        page_obj = post.get_page(page_number)
        context.update({
            'dash_user':dash_user,
            'dash_user_username':str(dash_user.username.username),
            'flo_unflo':check_follow(req_user, dash_user),
            'user_post':page_obj,
            'user_authenticated':user_authenticated,
            'req_user':req_user,
            'req_username':f'{req_user.username}'
        })
        return render(request, 'accounts/dashboard.html', context)

    else: # Authenticated user see their own dashboard
        nav_bar = UsersDetail.objects.select_related('username').prefetch_related('followers', 'userpost_set').filter(user_email=request.user.email).annotate(follower_count=Count('followers', distinct=True)).first()
        dash_user = nav_bar
        post = Paginator(dash_user.userpost_set.order_by('-publish_date'), 10)
        page_number = request.GET.get('page')
        page_obj = post.get_page(page_number)
        context.update({
            'dash_user':nav_bar,
            'dash_user_username':str(req_user.username),
            'flo_unflo':check_follow(req_user, dash_user),
            'user_post':page_obj,
            'user_authenticated':user_authenticated,
            'req_user':req_user,
            'req_username':str(req_user.username)
        })
        return render(request, 'accounts/dashboard.html', context)
        
    return render(request, 'accounts/login.html', context)

def notification(nav_bar, context):
    tm = nav_bar.notification_as_read
    notification = nav_bar.getnotification_set.filter(Q(mark_as_read_at__lte=datetime.now())).order_by('-mark_as_read_at').all() # I remove only() query because it's not import all fields
    unread_notification = notification.filter(Q(mark_as_read_at__gte=tm)).count()
    context.update({
            'nav_bar_user':nav_bar,
            'total_notification_count': notification.count(),
            'notification':notification,
            'unread_notification':unread_notification
        })
    return context

def login(request,slu = None):
    password = request.POST.get('password', None)
    pop_l = request.POST.get('pop_l', None)
    if request.user.is_authenticated:
        return redirect('/account/{0}/dashboard/'.format(str(request.user)))

    elif pop_l and request.method == 'POST' and request.is_ajax():
        data,status = pop_login(request)
        if data == 'success':
            return JsonResponse({'pop_login':True, 'success':True}, status = status)
        elif status == 400:
            return JsonResponse({'pop_login':True, 'false_message':'bad credential'}, status = status)

    elif password and request.method == 'POST':
        _ = request.get_full_path()
        username = request.POST.get('username', None)
        next_path = request.POST.get('next', _)
        # if not clean(request):
        #     messages.error(request,'Invalid reCaptcha!')
        #     return render(request,'account/login.html')
        if username is not None:
            username = User.objects.filter(Q(email = username)| Q(username = username)).first()
            user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            messages.success(request, 'You are logged in.')
            auth.login(request, user)
            if next_path.endswith('/login/'):
                return redirect(f'/account/{username}/dashboard/')
            elif next_path:
                return redirect(next_path)
            try:
                return HttpResponseRedirect(reverse(dashboard,args=[username],current_app='accounts'))
            except:
                return reverse(dashboard,args=[username])
        else:
            messages.error(request, 'bad credential')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')

def logout_member(request,slug = None):
    if request.user.is_authenticated and request.method == "POST":
        blog_view = request.session.get('blog_view', None)
        auth.logout(request)
        request.session['blog_view'] = blog_view
        messages.success(request, 'You are logged out.')
        return JsonResponse({'logout':True, 'path':str(request.path), 'success':True}, status = 200)
    else:
        messages.error(request, 'We are getting wrong url.')
        return redirect('login')

def pop_login(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
     # pop = request.POST.get('pop_login',None)
    # if not clean(request):
    #     messages.error(request,'Invalid reCaptcha!')
    #     return render(request,'account/login.html')
    if username != None and '.com' in username:
        username = User.objects.filter(email = username).first()
        user = auth.authenticate(request, username = username, password = password)
    else:
        user = auth.authenticate(request, username = username, password = password)
    if user is not None:
        blog_view = request.session.get('blog_view', None)
        auth.login(request,user)
        request.session['blog_view'] = blog_view
        return 'success', 200
    return 'bad credential', 400

def pop_register(request):
    p_register = PopUpForm(request.POST or None)
    if p_register.is_valid():
        password = p_register.cleaned_data['password']
        email = p_register.cleaned_data['email']
        username = email.split('@')[0]
        first_name = p_register.cleaned_data['first_name']
        last_name = p_register.cleaned_data['last_name']
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username = username,
            password = password, email = email)
        userdetail = UsersDetail.objects.create(First_name=first_name, Last_name=last_name, username = user, user_email = email)
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            return True, 'success'
    return p_register, 'errors'

def register(request, pop = None):
    userdetail = UsersDetailForm()
    pop_r = request.POST.get('pop_r', None)
    if request.user.is_authenticated:
        return redirect(f'/account/{str(request.user)}/dashboard/')
    elif request.method == 'POST' and pop_r:
        data, symbool = pop_register(request)
        if data == True and symbool == 'success':
            return JsonResponse({'pop_register':True, 'success':True}, status = 200)
        elif symbool == 'errors':
            return JsonResponse({'pop_register':True, "false_message":data.errors}, status = 400)
        else:
            return redirect('/')
    elif request.method == 'POST' and not pop_r:
        userdetail = UsersDetailForm(request.POST or None, request.FILES or None)
        if userdetail.is_valid():
            # if not clean(request):
            #     messages.error(request,'Invalid reCaptcha!')
            #     return render(request,'account/register.html',{'register':userdetail})
            # else:
            user = User.objects.create_user(username = userdetail.cleaned_data.get('user_email').strip().rsplit('@', 1)[0],
                password = userdetail.cleaned_data.get('password'),\
                email = userdetail.cleaned_data.get('user_email'), \
                first_name = userdetail.cleaned_data.get('First_name'), \
                last_name = userdetail.cleaned_data.get('Last_name'))
            userdetail = userdetail.save(commit=False)
            userdetail.username = user
            userdetail.save()
            messages.success(request,'You are registered,please log in.')
            return redirect('login')
        else:
            return render(request,'accounts/register.html',{'register':userdetail})
    return render(request,'accounts/register.html',{'register':userdetail})

@login_required
def update_user(request,slug = None):
    get_user = get_object_or_404(UsersDetail.objects.filter(user_email=request.user.email))

    if get_user:
        if request.method=='POST' and get_user.First_name:
            edit_form=UsersUpdateForm(request.POST or None,request.FILES or None,instance=get_user)
        elif request.method=='POST' and not get_user.First_name:
            edit_form=UsersUpdate2Form(request.POST or None,request.FILES or None,instance=get_user)
        elif not get_user.First_name:
            edit_form = UsersUpdate2Form(request.POST or None,instance=get_user)
        else:
            edit_form = UsersUpdateForm(request.POST or None,instance=get_user)
        if edit_form.is_valid():
            instance=edit_form.save(commit=False)
            instance.save()
            return redirect(f'/account/{str(request.user)}/dashboard/')
        return render(request,'accounts/register.html',{'register':edit_form, 'req_username':request.user.username, 'user_authenticated':request.user.is_authenticated, 'nav_bar_user':get_user})
    else:
        messages.error(request,'You have not permission')
        return redirect(f'/account/{str(request.user)}/dashboard/')

@login_required
def update_username(request):
    user = User.objects.filter(username=request.user.username)
    if request.method == "POST":
        username = request.POST.get('message')
        qs = User.objects.filter(username=username)
        data = {}
        if not check_uname(username):
            return JsonResponse({'success':False,'msz':'Invalid username'},status=400)
        if not qs.exists():
            user.update(username=username)
            return JsonResponse({'success':True,'name':username}, status=200)
            
        data.update({'success':False,'msz':'** This username already exists.'})
        return JsonResponse(data, status=400)
    pass


@login_required
def update_social_account(request, slug=None):
    if not slug == str(request.user.username):
        return redirect(f'/account/social/{str(request.user.username)}/update/')
    try:
        get_user = get_object_or_404(UsersDetail, user_email=str(request.user.email))
        return redirect(f'/account/{str(request.user.username)}/dashboard/')
    except:
        get_user = get_object_or_404(User, username=str(request.user.username))
        messages.warning(request,'Please update your account')
        edit_form = SocialUsersUpdateForm(request.POST or None, instance=get_user)
    if request.method == 'POST':
        edit_form = SocialUsersUpdateForm(request.POST or None, request.FILES or None)
        if edit_form.is_valid():
            instance=edit_form.save(commit=False)
            instance.username=request.user
            instance.save()
            return redirect(f'/account/{str(request.user.username)}/dashboard/')
        else:
            edit_form = SocialUsersUpdateForm(request.POST or None)
            return render(request,'accounts/register.html',{'register':edit_form})
    return render(request,'accounts/register.html',{'register':edit_form, 'req_username':request.user.username, 'user_authenticated':request.user.is_authenticated, 'nav_bar_user':get_user})

@login_required
def user_follow_toggle(request,slug=None):
    username = UsersDetail.objects.select_related().filter(user_email=request.user.email).first()
    if request.method == 'POST' and username:
        condition='follow'
        checkout=False
        try:
            checkout=isinstance(int(slug),int)
        except ValueError:
            checkout=False
        if not checkout:
            user = get_user(slug)
            uname = get_object_or_404(UsersDetail.objects.prefetch_related('followers'),username=user.first()).followers
            if uname and uname.all().filter(user_email=username.user_email).exists():
                uname.remove(username)
                condition = 'follow'
            else:
                uname.add(username)
                condition = 'unfollow'
            
            data={'condition': condition,
            'count': f'{uname.count()}',
            'slug':slug,
            'useracc':list(uname.all().values()),
            }
            return JsonResponse(data,status=200)
        elif checkout:
            uname = UsersDetail.objects.prefetch_related('followers__followers').filter(id=int(slug)).annotate(follower_count=Count('followers')).first()
            n=0
            nam = uname.followers.all()
            count = uname.follower_count
            data={
                'useracc':list(nam.values('id','First_name','Last_name','username__username'\
                    ,'profile_photo','interests'
                )),
                'username':str(request.user.username),
                'count':count,
                'refresh':True,
            }
            
            for _ in range(count):
                nam_id = nam[n].id
                data[f'follower_count_{nam_id}'] = nam[n].followers.count()
                if nam[n].followers.all().filter(user_email=request.user.email).exists():
                    data[f'follower_inside_{nam_id}']= "unfollow"
                else:
                    data[f'follower_inside_{nam_id}']= "follow"
                if nam[n].profile_photo:
                    data[f'follower_profile_{nam_id}'] = str(nam[n].profile_photo.url)
                n += 1
            return JsonResponse(data,status=200)
        else:
            messages.error(request,'Something went wrong please login/register with us')
            auth.logout(request)
            return JsonResponse({},status=400)
    else:
        messages.warning(request,'Invalid path provided.')
        return redirect(f'/account/social/{str(request.user.username)}/update/')

def get_user(slug):
    return User.objects.select_related().filter(username=slug)
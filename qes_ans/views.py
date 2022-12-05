from django.shortcuts import render, redirect
from django.utils.html import escape
from django.contrib import messages
from django.template.defaultfilters import urlize
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.forms import PopUpForm
from .models import QuestionAsked, AnswerBy, Discussion, DiscussionReply
from accounts.models import UsersDetail
from .form import QesAskedForm, AnsGivenForm

# Create your views here.

def get_qes_discussion(request, id=None, dis_from = None, start=0, end=3):
    if request.user.is_authenticated:
        usersdetail = UsersDetail.objects.filter(
            user_email=request.user.email).only('id').first() # gives TypeError here after logout
    else:
        usersdetail = None
    cr_prefetch = Prefetch('discussionreply_set', queryset=DiscussionReply.objects.select_related(
        'dis_reply_to', 'user').prefetch_related('dis_like_by').order_by('date_created'), to_attr='discussionreply_list')
    discuss = Discussion.objects.select_related('user').prefetch_related(
        'dis_like_by').prefetch_related(cr_prefetch).order_by('date_created')
    prefetch = Prefetch('discussion_set', queryset=discuss,
                        to_attr='discuss_list')
    if dis_from == 'qes_rom':
        dis = QuestionAsked.objects.filter(id=id).select_related(
            'qes_asked_by').prefetch_related(prefetch).first()
        data = {
            'req_username': request.user.username,
            'end': end,
            'user_authenticated': request.user.is_authenticated,
            'post_id': id,
            'post_slug_name': dis.slug_name,
            'post_author_username': ' '
        }
    elif dis_from == 'discuss_rom':
        dis = AnswerBy.objects.filter(id=id).prefetch_related(prefetch).first()
        data = {
            'req_username': request.user.username,
            'user_authenticated': request.user.is_authenticated,
            'post_id': id,
            'post_author_username': ' '
        }
    else:
        dis=None
    # seperate qestion model and answer model 
    if dis:
        n = 0
        for comment in dis.discuss_list:
            c_like = comment.dis_like_by.all()[:]
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

            for comment_repl in comment.discussionreply_list:
                z += 1
                cr_like = comment_repl.dis_like_by.all()[:]
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
                data[f'cr_reply_to_{n}_{z}'] = comment_repl.dis_reply_to.user_email.split(
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
    return JsonResponse({}, status=200)      

@login_required
def discussion_like_unlike(request, id, dis_type):
    usrs_dtl = UsersDetail.objects.filter(username=request.user).first()
    if request.method == 'POST':
        if dis_type == 'main_dis':
            dis = Discussion.objects.filter(id=id).prefetch_related('dis_like_by').first()
            return go_inside(request, usrs_dtl, dis)
        elif dis_type == 'reply_dis':
            dis = DiscussionReply.objects.filter(id=id).prefetch_related('dis_like_by').first()
            return go_inside(request, usrs_dtl, dis)
    else:
        return JsonResponse({'path': str(request.path)}, status=400)


def go_inside(request, usrs_dtl, dis):
    if usrs_dtl == dis.dis_like_by.filter(user_email=request.user.email).first():
        dis.dis_like_by.remove(usrs_dtl)
        condition = 'like'
    else:
        dis.dis_like_by.add(usrs_dtl)
        condition = 'unlike'

    data = {'condition': condition,
        'count': dis.dis_like_by.count()
    }

    return JsonResponse(data, status=200)


def discuss_q_and_a(request, discussion_type):
    if request.user.is_authenticated:
        dis_msz = urlize(escape(request.POST.get('message', None)), autoescape=True)
        print(dis_msz)
        q_id = request.POST.get('q_id', None)
        dis_id = request.POST.get('dis_id', None)
        reply_to = request.POST.get('reply_to', None)
        usr_dtl = UsersDetail.objects.filter(user_email = request.user.email).first()
        if request.method == 'POST' and discussion_type == 'main_dis_qes':
            qes = QuestionAsked.objects.filter(id = q_id).first()
            dis = Discussion.objects.create(q_asked = qes, text = dis_msz, user = usr_dtl, email = request.user.email)
            return JsonResponse({'success': True}, status=200)
        elif request.method == 'POST' and discussion_type == 'reply_dis_qes':
            usr_gt_rply = UsersDetail.objects.filter(user_email=reply_to + '@gmail.com').first()
            dis = Discussion.objects.filter(id = dis_id).first()
            rpl_dis = DiscussionReply.objects.create(discuss=dis, email=request.user.email, text=dis_msz, user=usr_dtl, dis_reply_to=usr_gt_rply)
            return JsonResponse({'success': True}, status=200)
        elif discussion_type == 'main_dis_ans':
            ans = AnswerBy.objects.filter(id=q_id).first()
            dis = Discussion.objects.create(a_given=ans, email=request.user.email, user=usr_dtl, text=dis_msz)
            # AnswerBy has no field named 'discussion_in_ans'
            return JsonResponse({'success':True}, status=200)
        elif discussion_type == 'reply_dis_ans':
            usr_gt_rply = UsersDetail.objects.filter(user_email=reply_to + '@gmail.com').first()
            dis = Discussion.objects.filter(id = dis_id).first()
            rpl_dis = DiscussionReply.objects.create(discuss=dis, email=request.user.email, text=dis_msz, user=usr_dtl, dis_reply_to=usr_gt_rply)
            return JsonResponse({'success': True}, status=200) 
            
    return JsonResponse({'path':'/account/login/'}, status=400)

@login_required
def discuss_delete(request, discussion_type, id):
    if id and discussion_type == 'main_dis':
        get_dis = Discussion.objects.filter(id=id).first()
        if get_dis.email == request.user.email:
            get_dis.delete()
            return JsonResponse({'success':True, 'text':'This content is no longer exist.'}, status=200)
        return JsonResponse({'success':False}, status=400)
    elif id and discussion_type == 'reply_dis':
        get_dis = DiscussionReply.objects.filter(id=id).first()
        if get_dis.email == request.user.email:
            get_dis.delete()
            return JsonResponse({'success':True, 'text':'This content is no longer exist.'}, status=200)
        return JsonResponse({'success':False}, status=400)

@login_required
def discuss_edit(request, discussion_type, id):
    message = urlize(escape(request.POST.get('message', None)))
    if id and discussion_type == 'main_dis' and message:
        get_dis = Discussion.objects.filter(id = id).first()
        if get_dis.email == request.user.email:
            get_dis.text = message
            get_dis.save()
            return JsonResponse({'success':True, 'text':message}, status=200)
        return JsonResponse({'success':True}, status=200)

    elif id and discussion_type == 'reply_dis' and message:
        get_dis = DiscussionReply.objects.filter(id = id).first()
        if get_dis.email == request.user.email:
            get_dis.text = message
            get_dis.save()
            return JsonResponse({'success':True, 'text':message}, status=200) 
        return JsonResponse({'success':True}, status=200)
    else:
        return redirect('/')


@login_required
def question_asked(request):
    q_form = QesAskedForm()
    qs = QuestionAsked.objects.filter(qes_asked_by=request.user)
    if request.method == "POST":
        q_form = QesAskedForm(request.POST or None)
        instance = q_form.save(commit=False)
        instance.qes_asked_by = request.user
        instance.save()
        return redirect(f'/account/{str(request.user.username)}/dashboard/#question-asked-button')
    req_username = request.user
    user_authenticated = req_username.is_authenticated
    context = {'q_form':q_form, 'question':qs, 'req_username': str(req_username),
                        'user_authenticated': user_authenticated}
    return render(request, 'qes_ans/q_and_a.html', context)

@login_required
def edit_question(request, id):
    qs = QuestionAsked.objects.filter(id=id).first()
    if qs and qs.qes_asked_by == request.user:
        q_form = QesAskedForm(request.POST or None, instance=qs)
        req_username = request.user
        user_authenticated = req_username.is_authenticated
        context = {'q_form':q_form, 'question':qs, 'req_username': str(req_username),
                            'user_authenticated': user_authenticated}
        if request.method == "POST" and q_form.is_valid():
            q_form.save()
            return redirect(f'/account/{str(request.user.username)}/dashboard/#question-asked-button')
        return render(request, 'qes_ans/q_and_a.html', context)
    messages.error(request, 'We did not find query related to you')
    return redirect(f'/account/{request.user.username}/dashboard/')


@login_required
def edit_answer(request, id):
    ans = AnswerBy.objects.select_related('q_asked').filter(id=id).first()
    usr_dtl = UsersDetail.objects.filter(user_email=request.user.email)
    if ans and ans.ans_given_by.all()[0] == usr_dtl.first():
        qs = ans.q_asked
        a_form = AnsGivenForm(request.POST or None, instance=ans)
        req_username = request.user
        user_authenticated = req_username.is_authenticated
        context = {'a_form':a_form, 'question':qs, 'ans_id':ans.id, 'req_username': str(req_username),
                            'user_authenticated': user_authenticated}
        if request.method == "POST" and a_form.is_valid():
            a_form.save()
            return redirect(f'/q/{qs.id}/{qs.slug_name}/answer/')
        return render(request, 'qes_ans/edit_answer.html', context)
    messages.error(request, 'We did not find query related to you')
    return redirect(f'/account/{request.user.username}/dashboard/')

@login_required
def delete_answer(request, id):    
    ans = AnswerBy.objects.filter(id=id).first()
    usrs_dtl = UsersDetail.objects.filter(user_email=request.user.email).first()
    if ans and ans.ans_given_by.filter(user_email=usrs_dtl.user_email).exists():
        q_id, q_slug = ans.q_asked.id, ans.q_asked.slug_name
        ans.delete()
        messages.success(request, 'successfully deleted')
        return redirect(f'/q/{q_id}/{q_slug}/answer/')
    messages.warning(request, 'we get nothing for your query')
    return redirect('/')    
        

def answer_given(request):
    q_id = request.POST.get('q_id', None)
    qes = QuestionAsked.objects.filter(id=q_id).first()
    if request.user.is_authenticated and request.method == "POST":
        ansr = AnsGivenForm(request.POST or None)
        usrs_dtl = UsersDetail.objects.filter(username=request.user).first()
        if ansr.is_valid():
            instance = ansr.save(commit = False)
            instance.q_asked = qes
            instance.save()
            instance.ans_given_by.add(usrs_dtl)
        return redirect(f'/q/{q_id}/{qes.slug_name}/answer/')
    else:
        return redirect('login')

def all_answers(request, id, q_title):
    qs = QuestionAsked.objects.select_related('qes_asked_by').filter(id=id).annotate(ans_count=Count('answerby')).first()
    if qs:
        rel_qes = QuestionAsked.objects.select_related().filter(tag__icontains=qs.tag).exclude(slug_name=qs.slug_name)[:10]
        a_form = AnsGivenForm()
        prefetch = Prefetch('ans_given_by', queryset=UsersDetail.objects.select_related('username'), to_attr='ans_user')
        ans = AnswerBy.objects.prefetch_related(prefetch).filter(q_asked = qs, selected_ans=True)
        from itertools import chain
        ans_2 = AnswerBy.objects.prefetch_related(prefetch).order_by('date_created').filter(q_asked = qs, selected_ans=False)
        ans = chain(ans, ans_2)
        context = {'a_form':a_form,'rel_qes':rel_qes, 'question':qs, 'answer':ans, 'pop_form':PopUpForm(),'ans_count':qs.ans_count}
        if request.user.is_authenticated:
            req_username = request.user
            user_authenticated = req_username.is_authenticated
            context.update({'req_username': req_username,
                                'user_authenticated': user_authenticated})
        return render(request, 'qes_ans/answers.html', context)
    return redirect('/')

@login_required
def select_answer(request, id, q_id):
    _ = request.get_full_path()
    qes = QuestionAsked.objects.filter(id=q_id).prefetch_related('answerby_set').first()
    ans = qes.answerby_set.all().filter(selected_ans=True)
    s_ans = AnswerBy.objects.filter(id=id)
    if ans.first() and qes.qes_asked_by == request.user:
        ans.update(selected_ans=False)
    s_ans.update(selected_ans=True)
    return redirect(_)

@login_required
def delete_question(request, id):
    qs = QuestionAsked.objects.filter(id=id).first()
    if qs and qs.qes_asked_by == request.user:
        qs.delete()
        messages.success(request, 'question was deleted', fail_silently=True)
        return redirect(f'/account/{str(request.user.username)}/dashboard/')
    messages.warning(request, 'we did not find your query.')
    return redirect(f'/account/{str(request.user.username)}/dashboard/#question-asked-button')
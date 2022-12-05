from blog.models import GetNotification

def update_notification(request, fn, extra, text=None, id=None):
    if fn == 'publish_post':
        text = f'{extra.author.username} added new post :- {extra.blog_title}'
        for follow in extra.author.followers.all():
            if request.user != follow.username:
                notify = GetNotification(user_notify = follow, text = text, text_url = f'http://127.0.0.1:8000/{extra.author.username}/detail/{extra.slug_name}/')
                notify.save()

    elif fn == 'public_comment_main':
        usr = []
        all_reltd_comment = extra['all_reltd_comment'] #it contains userpost related comment
        post = extra['post']
        comment_connected = all_reltd_comment.filter(id = id).first()
        text1 = f"Someone commented on {post.author.username}'s post:- '{text}'"
        for user_comment in all_reltd_comment:
            if request.user != user_comment.user.username and (user_comment.user not in usr) and post.author not in usr:
                usr.append(user_comment.user)
                notify = GetNotification(user_notify = user_comment.user, comment = comment_connected, text = text1, text_url = f'http://127.0.0.1:8000/{post.author.username}/detail/{post.slug_name}/#reply_comment_5008{id}')
                notify.save()
        if request.user != post.author.username and post.author not in usr:
            text2 = f"Someone commented on your post:- '{text}'"
            usr.append(post.author)
            notify = GetNotification(user_notify = post.author, comment = comment_connected,  text = text2, text_url = f'http://127.0.0.1:8000/{post.author.username}/detail/{post.slug_name}/#reply_comment_5008{id}')
            notify.save()

    elif fn == 'public_comment_reply':
        print(request.get_host(), request.path)
        text1 = f"{request.user} commented on a post you follow :- '{text}'"
        text2 = f"{request.user} reply to your comment:- {text}"
        usr_get_reply = extra['rep_user']
        if request.user.is_authenticated and usr_get_reply.username == request.user.username:
            text2 = f"You reply to your own comment:- {text}"
        post = extra['post']
        div_comment = extra['div_comment']
        comment_connected = div_comment.commentreply_set.filter(id=id).first()
        usr = []
        for child_reply in div_comment.commentreply_set.all(): #'div_comment' is particular section of whole comment
            if child_reply.reply_to == usr_get_reply.usersdetail and child_reply.reply_to not in usr:
                usr.append(child_reply.reply_to)
                print(child_reply, ' -1st')
                notify = GetNotification(user_notify=usr_get_reply.usersdetail, comment=div_comment, comment_reply=comment_connected,  text=text2, text_url=f'http://127.0.0.1:8000/{post.author.username}/detail/{post.slug_name}/#reply_comment_1008{id}')
                notify.save()

            elif request.user != child_reply.user.username and child_reply.user not in usr:
                usr.append(child_reply.user)
                print(child_reply,' -2nd')
                notify = GetNotification(user_notify=child_reply.user, comment=div_comment, comment_reply=comment_connected, text=text1, text_url=f'http://127.0.0.1:8000/{post.author.username}/detail/{post.slug_name}/#reply_comment_1008{id}')
                notify.save()

    elif fn == 'post_edit':
        usr=[]
        text = f'{extra.author.username} edited their post:- {extra.blog_title}'
        for follow in extra.author.followers.all():
            usr.append(follow)
            notify = GetNotification(user_notify = follow, text = text, text_url = f'http://127.0.0.1:8000/{extra.author.username}/detail/{extra.slug_name}/')
            notify.save()

        text = f'{extra.author.username} edited the post you follow:- {extra.blog_title}'
        for comment in extra.comment_set.all():
            if comment.user.username != request.user and comment.user not in usr:
                usr.append(comment.user)
                notify = GetNotification(user_notify = comment.user, text = text, text_url = f'http://127.0.0.1:8000/{extra.author.username}/detail/{extra.slug_name}/')
                notify.save()

    elif fn == 'user_follow_toggle':
        # uname = extra['notify_uname']
        # follower_uname = extra['follower_uname']
        # notify = GetNotification(user_notify = uname, text = text, text_url = f'http://127.0.0.1:8000/account/{follower_uname}/dashboard/')
        # notify.save()
        pass

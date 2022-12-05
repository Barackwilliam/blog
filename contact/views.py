from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Contact
from django.contrib import messages

# Create your views here.
def contact(request):
    if request.method == "POST" and request.is_ajax():
        email   = request.POST.get('email',None)

        already_contacted = Contact.objects.filter(email=email)
        if already_contacted:
            messages.warning(request,'Hi, {0} you already subscribed.'.format(email))
            return JsonResponse({'contact':True,'path':str(request.path),'message':'Hi, {0} you already subscribed.'.format(email)},status=400)
        else:
            contact = Contact(email=email)
            contact.save()
            messages.success(request,'Hi, {0} Thanks for subscribe.'.format(email))
            return JsonResponse({'contact':True,'path':str(request.path),'success':True},status=200)
    return redirect('/')

from django.shortcuts import render, redirect
from urllib.parse import urlparse
from django.http import JsonResponse, Http404
from blog.utils import random_string_gen
from .models import ShortLink

def link_gen():
    gen = random_string_gen(size=4)
    qs = ShortLink.objects.filter(shorter_url=gen)
    if qs.exists():
        link_gen()
    return gen

def find_post(request, pl=None):
    post_link = ShortLink.objects.filter(shorter_url=pl).first()
    if post_link:
        link = f"{post_link.url_link}"
        return redirect(link)
    else:
        raise Http404('wrong')

def generate_post_link(request):
    if request.method == 'POST':
        url_name = request.POST.get('url', None)
        path = request.build_absolute_uri()
        l_schema, host_name = urlparse(path)[:2]
        if url_name and len(url_name) < 445:
            rand_gen = link_gen()
            gen = f'{l_schema}://{host_name}/v/{rand_gen}/'
            short_link = ShortLink.objects.create(url_link=url_name, shorter_url=rand_gen)
            data = {'link':gen}
        else:
            data = {'link' : 'Url length not exceeds 500 characters. :('}
        return JsonResponse(data, status=200)
    return JsonResponse({}, status=200)


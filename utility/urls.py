from django.urls import include, path, re_path
from .views import find_post, generate_post_link

urlpatterns = [
    path('gen/', generate_post_link, name='generate_post_link'),
    path('<slug:pl>/', find_post, name='find_link'),
]
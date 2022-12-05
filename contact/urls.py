from django.urls import re_path
from .views import contact

urlpatterns = [
    re_path(r'^$',contact,name='contact'),
    ]

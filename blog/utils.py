import random
import string
from django.utils.text import slugify

def random_string_gen(size=10, char=string.digits + string.ascii_lowercase):
    return ''.join(random.choice(char) for _ in range(size))

def slug_generator(instance, new_slug=None):
    Klass = instance.__class__
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.blog_title)
    qs = Klass.objects.filter(slug_name=slug.capitalize())
    if qs.exists():
        slug = '{0}-{1}'.format(slug,random_string_gen(size=5))
        return slug_generator(instance, new_slug=slug)
    return slug.capitalize()
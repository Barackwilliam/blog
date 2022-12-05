from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import UserPost
from django.core.exceptions import ValidationError
from PIL import Image,ImageSequence
# from django.contrib import messages
# from django.contrib.auth.models import User
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from sys import getsizeof


def image_cutter(blog_image):
    if blog_image:
        im = Image.open(blog_image)
        if blog_image.size>153600:
            return 'error'
        elif im.height>800 or im.width>800:
            return 'error'
        elif im.height<200 or im.width<200:
            return 'error'
        else:
            return blog_image
    return 'error'

SELECT = (
    ('Programming','Programming'),
    ('Science','Science'),
    ('History','History'),
    ('Tech','Tech Trick'),
    ('Android','Android'),
    ('Discovery','Discovery'),
    ('Other','Other')
)

class PostForm(forms.ModelForm):
    category = forms.ChoiceField(choices = SELECT,label = 'Choose a category')
    category.widget.attrs.update({'class' : 'form-control'})
    class Meta:
        model = UserPost
        fields = ('blog_title', 'blog_image', 'image_credit', 'blog_description', 'reading_time', 'tag')
        widgets = {
            'blog_title':forms.TextInput(attrs = {'class':'form-control','placeholder':'Title'}),
            'blog_image':forms.FileInput(attrs = {'class':'form-control'}),
            'image_credit':forms.URLInput(attrs = {'class':'form-control','placeholder':'https://www.pexels.com/photo/black-flat-screen-computer-monitor-1714208/'}),
            'blog_description':CKEditorUploadingWidget(),
            'tag':forms.TextInput(attrs = {'class':'form-control','placeholder':'url,python,django....etc'}),
            'reading_time': forms.NumberInput(attrs = {'class':'form-control','min':0,'name':'minutes'})
        }


    def clean_blog_image(self):
        blog_image = self.cleaned_data.get('blog_image')
        if blog_image:
            data = image_cutter(blog_image)
            if data == 'error':
                raise ValidationError('Image size (200*200 < image < 800*800) and below 150KB')
            else:
                return data
        raise ValidationError('Image size (200*200 < image < 800*800) and below 150KB')

    def clean_blog_description(self):
        blog_description = self.cleaned_data.get('blog_description')
        if blog_description:
            blog_description = blog_description.replace("<img","<img class='img-fluid' alt='Responsive image'")
            blog_description = blog_description.replace('<pre',"<pre class='text-white bg-secondary'")
            return blog_description
        return blog_description

class PostEditForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('blog_description','reading_time','tag')
        widgets = {
            'blog_description':CKEditorUploadingWidget(),
            'tag':forms.TextInput(attrs = {'class':'form-control','placeholder':'url,python,django....etc'}),
            'reading_time': forms.NumberInput(attrs = {'class':'form-control','min':0,'name':'minutes'})
        }

    def clean_blog_description(self):
        blog_description = self.cleaned_data.get('blog_description')
        if blog_description:
            blog_description = blog_description.replace("<img","<img class='img-fluid' alt='Responsive image'")
            blog_description = blog_description.replace('<pre',"<pre class='text-white bg-secondary'")
            return blog_description
        return blog_description

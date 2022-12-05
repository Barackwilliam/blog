from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.html import escape
from .models import UsersDetail
import re
# from PIL import Image,ImageSequence
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from sys import getsizeof


# def image_cutter():
#     def cutter(blog_image):
#         ext = ['.gif','.jpg','.JPG','.png','.PNG']
#         valid=False
#         # cnt=0
#         for i in ext:
#             cnt+=1
#             if i in str(blog_image).partition(i):
#                 # if cnt==1:
#                 #     break
#                 valid = True
#             break
#         if valid and blog_image:
#             im = Image.open(blog_image)
#             if blog_image.size>81920:
#                 raise forms.ValidationError('Image size (300*250 < image < 500*500) and below 80KB')
#             elif im.height>500 or im.width>500:
#                 # print(blog_image.name.split('.')[0])
#                 im1=im.resize((500,500))
#                 output = BytesIO()
#
#                 im1.save(output, im.format)
#                 blog_image=InMemoryUploadedFile(output,'ImageField', "%s.png" %blog_image.name.split('.')[0], 'blog_image/png',getsizeof(output), None)
#                 return blog_image
#             elif im.height<300 or im.width<200:
#                 # messages.error(self.request,'2 Image must be between 500*300>image<800*600')
#                 raise forms.ValidationError('Image size (300*200 < image < 850*700) and below 80KB')
#             else:
#                 return blog_image
        # elif cnt==1:
        #     size = 320, 240
        #     # Open source
        #     im = Image.open(blog_image)
        #     # Get sequence iterator
        #     frames = ImageSequence.Iterator(im)
        #     return blog_image
            # def thumbnails(frames):
            #     for frame in frames:
            #         thumbnail = frame.copy()
            #         thumbnail.thumbnail(size, Image.ANTIALIAS)
            #         yield thumbnail
            #
            #     frames = thumbnails(frames)
            #
            #     # Save output
            #     om = next(frames) # Handle first frame separately
            #     om.info = im.info # Copy sequence info
            #     om.save("out.gif", save_all=True, append_images=list(frames))
        # else:
        #     pass
    # return cutter
    # else:
    #     print('non')
    #     raise forms.ValidationError('1Image size (300*200 < image < 850*700) and below 80KB')


class UsersDetailForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    class Meta:
        model = UsersDetail
        fields = ['First_name','Last_name','user_email','interests','about',
        'thought','profile_photo','youtube_url','github_url','linkedin_url','facebook_url']
        widgets={
            'First_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First name','required':'This field is required'}),
            'Last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last name','required':'This field is required'}),
            'user_email':forms.TextInput(attrs={'class':'form-control','placeholder':'xyz@domain.com'}),
            'interests':forms.TextInput(attrs={'class':'form-control','placeholder':'Physics,Python programming,Artificial Intelligence'}),
            'about':forms.Textarea(attrs={'class':'form-control','rows':8,'cols':40,
            'placeholder':'About yourself e.g, I loves programming.I had given several papers in different level...etc'}),
            'thought':forms.TextInput(attrs={'class':'form-control','placeholder':'Practice makes man perfect'}),
            'profile_photo':forms.FileInput(attrs={'class':'form-control','placeholder':'Upload photo'}),
            'youtube_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Youtube link if any'}),
            'github_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Github link if any'}),
            'linkedin_url':forms.TextInput(attrs={'class':'form-control','placeholder':'linkedin link if any'}),
            'facebook_url':forms.TextInput(attrs={'class':'form-control','placeholder':'facebook link if any'}),
        }


    def clean_user_email(self):
        email=self.cleaned_data.get("user_email")
        qs = User.objects.filter(Q(email=email)| Q(username=email.strip().rsplit('@', 1)))
        if qs.exists():
            raise forms.ValidationError("** Username with this email already exists.")
        return email

    def clean_First_name(self):
        First_name = self.cleaned_data.get('First_name')
        print(First_name)
        if not check_uname(First_name):
            raise forms.ValidationError('Invalid First name')
        return First_name

    def clean_Last_name(self):
        Last_name = self.cleaned_data.get('Last_name')
        print('109: ',check_uname(Last_name))
        if not check_uname(Last_name):
            raise forms.ValidationError('Invalid Last name')
        return Last_name

    def clean_about(self):
        return escape(self.cleaned_data.get("about"))

    def clean_thought(self):
        return escape(self.cleaned_data.get('thought'))
    # def clean_profile_photo(self):
    #     try:
    #         blog_image=self.cleaned_data.get('profile_photo')
    #         if blog_image:
    #             data = image_cutter()(blog_image)
    #             return data
    #     except:
    #         pass

class UsersUpdateForm(forms.ModelForm):
    class Meta:
        model = UsersDetail
        fields = ['interests','about','profile_photo','thought','youtube_url','github_url','linkedin_url','facebook_url']
        widgets={
            'interests':forms.TextInput(attrs={'class':'form-control','placeholder':'Physics,Python programming,Artificial Intelligence'}),
            'about':forms.Textarea(attrs={'class':'form-control','rows':8,'cols':40,
            'placeholder':'About yourself e.g, I loves programming.I had given several papers in different level...etc'}),
            'profile_photo':forms.FileInput(attrs={'class':'form-control','placeholder':'Upload photo'}),
            'thought':forms.TextInput(attrs={'class':'form-control','placeholder':'Practice makes man perfect'}),
            'youtube_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Youtube link if any'}),
            'github_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Github link if any'}),
            'linkedin_url':forms.TextInput(attrs={'class':'form-control','placeholder':'linkedin link if any'}),
            'facebook_url':forms.TextInput(attrs={'class':'form-control','placeholder':'facebook link if any'}),
        }

    def clean_about(self):
        return escape(self.cleaned_data.get("about"))

    def clean_thought(self):
        return escape(self.cleaned_data.get('thought'))
    
    def clean_First_name(self):
        First_name = self.cleaned_data.get('First_name')
        if not check_uname(First_name):
            raise forms.ValidationError('Invalid First name')
        return First_name

    def clean_Last_name(self):
        Last_name = self.cleaned_data.get('Last_name')
        if not check_uname(Last_name):
            raise forms.ValidationError('Invalid Last name')
        return Last_name

    # def clean_profile_photo(self):
    #     try:
    #         blog_image=self.cleaned_data.get('profile_photo')
    #         if blog_image:
    #             data = image_cutter()(blog_image)
    #             return data
    #     except:
    #         pass


class UsersUpdate2Form(forms.ModelForm):
    class Meta:
        model = UsersDetail
        fields = ['First_name','Last_name','interests','about','profile_photo','thought','youtube_url','github_url','linkedin_url','facebook_url']
        widgets={
            'First_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First name','required':'This field is required'}),
            'Last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last name','required':'This field is required'}),
            'interests':forms.TextInput(attrs={'class':'form-control','placeholder':'Physics,Python programming,Artificial Intelligence'}),
            'about':forms.Textarea(attrs={'class':'form-control','rows':8,'cols':40,
            'placeholder':'About yourself e.g, I loves programming.I had given several papers on different level...etc'}),
            'thought':forms.TextInput(attrs={'class':'form-control','placeholder':'Practice makes man perfect'}),
            'profile_photo':forms.FileInput(attrs={'class':'form-control','placeholder':'Upload photo'}),
            'youtube_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Youtube link if any'}),
            'github_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Github link if any'}),
            'linkedin_url':forms.TextInput(attrs={'class':'form-control','placeholder':'linkedin link if any'}),
            'facebook_url':forms.TextInput(attrs={'class':'form-control','placeholder':'facebook link if any'}),
        }

    def clean_about(self):
        return escape(self.cleaned_data.get("about"))

    def clean_thought(self):
        return escape(self.cleaned_data.get('thought'))

    def clean_First_name(self):
        First_name = self.cleaned_data.get('First_name')
        if not check_uname(First_name):
            raise forms.ValidationError('Invalid First name')
        return First_name

    def clean_Last_name(self):
        Last_name = self.cleaned_data.get('Last_name')
        if not check_uname(Last_name):
            raise forms.ValidationError('Invalid Last name')
        return Last_name

    # def clean_profile_photo(self):
    #     try:
    #         blog_image=self.cleaned_data.get('profile_photo')
    #         if blog_image:
    #             data = image_cutter()(blog_image)
    #             return data
    #     except:
    #         pass

class SocialUsersUpdateForm(forms.ModelForm):
    class Meta:
        model = UsersDetail
        fields = ['First_name','Last_name','user_email','interests','about','profile_photo','thought','youtube_url','github_url','linkedin_url','facebook_url']
        widgets={
            'First_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First name','required':'This field is required'}),
            'Last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last name','required':'This field is required'}),
            'user_email':forms.TextInput(attrs={'class':'form-control','placeholder':'xyz@domain.com'}),
            'interests':forms.TextInput(attrs={'class':'form-control','placeholder':'Physics,Python programming,Artificial Intelligence'}),
            'about':forms.Textarea(attrs={'class':'form-control','rows':8,'cols':40,
            'placeholder':'About yourself e.g, I loves programming.I had given several papers in different level...etc'}),
            'thought':forms.TextInput(attrs={'class':'form-control','placeholder':'Practice makes man perfect'}),
            'profile_photo':forms.FileInput(attrs={'class':'form-control','placeholder':'Upload photo'}),
            'youtube_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Youtube link if any'}),
            'github_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Github link if any'}),
            'linkedin_url':forms.TextInput(attrs={'class':'form-control','placeholder':'linkedin link if any'}),
            'facebook_url':forms.TextInput(attrs={'class':'form-control','placeholder':'facebook link if any'}),
        }


    def clean_email(self):
        email=self.cleaned_data.get("user_email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("** Email already exists")
        return email
    def clean_about(self):
        return escape(self.cleaned_data.get("about"))

    def clean_First_name(self):
        First_name = self.cleaned_data.get('First_name')
        if not check_uname(First_name):
            raise forms.ValidationError('Invalid First name')
        return First_name

    def clean_Last_name(self):
        Last_name = self.cleaned_data.get('Last_name')
        if not check_uname(Last_name):
            raise forms.ValidationError('Invalid Last name')
        return Last_name

    def clean_thought(self):
        return escape(self.cleaned_data.get('thought'))

def check_uname(value):
    if not re.match('^[.a-zA-Z0-9_]+$', value):
        return None
    return value

class PopUpForm(forms.Form):
    first_name = forms.CharField(label='First name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'first name'}))
    last_name = forms.CharField(label='Last name',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'last name'}))
    email    = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'xyz@gmail.com'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("** Your password must be same")
        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not check_uname(first_name):
            raise forms.ValidationError('Invalid First name')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not check_uname(last_name):
            raise forms.ValidationError('Invalid Last name')
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_uname_ok = check_uname(email.split('@')[0])
        if not is_uname_ok:
            raise forms.ValidationError('** Email must be in gmail.com only')
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise forms.ValidationError("** Email already exists")
        if 'gmail.com' in email:
            return email
        else:
            raise forms.ValidationError('** Email must be in gmail.com only')

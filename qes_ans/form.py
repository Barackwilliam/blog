from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import QuestionAsked, AnswerBy

class QesAskedForm(forms.ModelForm):
    class Meta:
        model = QuestionAsked
        fields = ['title', 'qes', 'tag']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'What is index in list?','required':'This field is required'}),
            'qes':CKEditorUploadingWidget(),
            'tag':forms.TextInput(attrs={'class':'form-control','placeholder':'python, C++','required':'This is required'})
        }

    def clean_ans(self):
        return check_ans(self.cleaned_data.get('qes'))

class AnsGivenForm(forms.ModelForm):
    class Meta:
        model = AnswerBy
        fields = ['ans']
        widgets={
            'ans':CKEditorUploadingWidget()
        }

    def clean_ans(self):
        return check_ans(self.cleaned_data.get('ans'))

def check_ans(data):
    ans = data
    if ans:
        ans = ans.replace('<pre',"<pre class='text-white bg-secondary'")
        return ans
    return ans

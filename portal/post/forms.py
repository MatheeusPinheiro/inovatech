from django import forms
from django.conf import settings 
from .models import Post,PostComment

class PostForm(forms.ModelForm):  
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'},),
        input_formats=settings.DATE_INPUT_FORMATS
        ) 
 
    #published_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',})) 
    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        del self.fields['user'] 
        del self.fields['created_date']
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 
            if field_name == 'activate_post':
                field.widget.attrs['class'] = 'form-check-input'


class PostCommentForm(forms.ModelForm):
    class Meta:
        model= PostComment
        fields=['comment']

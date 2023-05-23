from django import forms 
from perfil.models import Profile   

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
 
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        del self.fields['user']   
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 
import re
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm, PasswordResetForm, SetPasswordForm, AuthenticationForm
from django.core.exceptions import ValidationError 
from contas.models import MyUser  
 
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password.""" 
    
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
      
    class Meta:
        model = MyUser
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active')  
        help_texts = {'username': None}
        labels = {
            'email': 'Email', 
            'username': 'Username', 
            'first_name': 'Primeiro Nome', 
            'last_name': 'Sobrenome', 
            'is_active': 'Usúario Ativo?'
        }
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'is_active' : forms.HiddenInput(attrs={'class': 'form-check-input'}),
        } 
        
    def __init__(self, user=None, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)   
    

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print("Usuario Cadastrado !")
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    def __init__(self, user=None, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)  
        if not user.type_user in ['ad','co']:
            del self.fields['is_active'] 
            del self.fields['type_user'] 
        else:
            print("Usúario Padrão") 
        
    class Meta:
        model = MyUser
        fields = ('email', 'username', 'first_name', 'last_name', 'type_user', 'is_active')
        help_texts = {'username': None}
        labels = {
            'email': 'Email', 
            'username': 'Username', 
            'first_name': 'Primeiro Nome', 
            'last_name': 'Sobrenome', 
            'type_user': 'Tipo de Usúario',
            'is_active': 'Usúario Ativo?'
        }
        widgets = {
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'type_user' : forms.Select(attrs={'class': 'form-control'}),
            'is_active' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        } 
        
class UserLoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        
    username = forms.CharField(label="Digite seu email:", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Digite sua senha:", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
    

class UserPasswordChangeForm(PasswordChangeForm):
    
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        
    old_password = forms.CharField(label="Senha antiga:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))    
    new_password1 = forms.CharField(label="Senha nova:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Confirmação da senha nova:",widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        
    email = forms.EmailField(label="Digite seu Email:", max_length=254, widget=forms.EmailInput(attrs={'class':'form-control','autocomplete': 'email'}) )


class UserPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetConfirmForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(label="Senha nova:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Confirmação da senha nova:",widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
    
class UserAdmin(BaseUserAdmin):   
    list_display = ('email', 'username', 'first_name', 'last_name', 'type_user', 'is_active', 'is_admin')
    readyonly_fields = ['date_joined']
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'type_user')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ) 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
     
    
admin.site.register(MyUser, UserAdmin)  
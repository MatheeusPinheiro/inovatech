import re
from urllib import request
from django.conf import settings
from django.contrib.auth.views import LoginView 
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse, reverse_lazy  
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from contas.admin import UserCreationForm, UserLoginForm, UserChangeForm
from contas.models import MyUser    
from django.contrib.auth.mixins import LoginRequiredMixin   
from contas.base_admin_permissions import BaseAdminUserAd, BaseAdminUserCo, BaseAdminUserall
from django.core.mail import send_mail
from django.template.loader import render_to_string

class UserLoginView(SuccessMessageMixin,LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    success_url = '/post-list/'
    success_message = "Login efetuado com sucesso." 
    
  
class UserCreateView(SuccessMessageMixin, CreateView):
    model = MyUser
    form_class = UserCreationForm
    template_name = 'registration/user_new.html'
    success_url = reverse_lazy('home')
    success_message = "Cadastro efetuado com sucesso."  
    
    def get(self,request,*args,**kwargs):
        self.object = None
        return super().get(request,*args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        self.object = None
        
        context = {
           'email': request.POST.get('email'),
           'username': request.POST.get('username')
        }
        body = "Olá, o usuário "+context['username'] +" se registrou no sistema. Clique no link abaixo para aprovar seu cadastro"
        
        html_string = render_to_string('sendmail/send_regist.html', context)
        html_body = html_string.format(**context)
        
        send_mail(
            'Um novo usuário se registrou no sistema!',
            body,
            settings.DEFAULT_FROM_EMAIL,
            ['matheuspinheiro0597@gmail.com'],
            html_message= html_body,
            fail_silently=False,
        )
        print(context['username'])
        return super().post(request,*args, **kwargs)
        
    
class UserUpdateView(SuccessMessageMixin, BaseAdminUserCo, LoginRequiredMixin, UpdateView): 
    model = MyUser
    form_class = UserChangeForm
    template_name = 'registration/user_new.html'
    success_url = reverse_lazy('home')
    success_message = "Update efetuado com sucesso."    
    
    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get(self,request,*args,**kwargs):
        self.object = None
        return super().get(request,*args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        self.object = None
        context = {
            'email': request.POST.get('email'),
            'fisrt_name': request.POST.get('first_name'),
            'is_active': request.POST.get('is_active')
        }
        
        if context['is_active'] == 'on' or context['is_active'] == True:
            if self.model.objects.filter(email=context['email'], is_active=True).exists():
                print('1 - Usuário já ativo na plataforma')
            else:
                print('2 - Usuário ativo, E-mail enviado para o usuário')
                body = "Olá, o usuário "+context['fisrt_name'] +" Seu cadastro foi aprovado no sistema."
                
                       
                html_string = render_to_string('sendmail/send_aprova.html', context)
                html_body = html_string.format(**context)
                
                send_mail(
                'Seu cadastro foi aprovado no sistema!',
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['matheuspinheiro0597@gmail.com', (context['email'])],
                html_message= html_body,
                fail_silently=False,
                )   
                print('E-mail enviado!')
                
            return super().post(request,*args, **kwargs)
                
  
class Timeout(TemplateView):
    template_name = 'registration/timeout.html'
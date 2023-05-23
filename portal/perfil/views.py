from typing import Any, Optional
from django.db import models
from django.shortcuts import render
from contas.models import MyUser
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy 

from post.models import Post
from perfil.models import Profile
from perfil.forms import ProfileForm
# Create your views here.

class ProfileView(DetailView):
    model = MyUser
    template_name = "profile.html"
    context_object_name = "perfil"
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def get_object(self, queryset=None):
        self.perfil = self.model.objects.select_related('profile').prefetch_related('posts').get(username=self.kwargs.get(self.slug_url_kwarg))
        return self.perfil
    
    def get(self, request, *args, **kwargs):
       self.object = self.get_object()
       context = self.get_context_data(object=self.object)
       context['get_posts'] = Post.objects.filter(user=self.object, activate_post=True)
       return self.render_to_response(context)
   
   
class ProfileEditView(UpdateView):
    model = Profile 
    form_class = ProfileForm
    template_name = "profile_edit.html"
    context_object_name = "profile"  

    def get_object(self, queryset=None):
        return self.request.user.profile 

    def get_success_url(self):  
        messages.success(self.request, 'O Perfil foi atualizado com sucesso')
        return reverse_lazy('user-profile', args=[self.object.user.username])
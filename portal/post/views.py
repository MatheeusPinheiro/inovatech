from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.db import models, transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from contas.base_admin_permissions import BaseAdminUserCo
from django.contrib import messages
from django.shortcuts import redirect, render 

from contas.models import MyUser
from .forms import PostForm, PostCommentForm
from .models import Post, PostComment 

class InitialListView(ListView):
    model = Post
    template_name='home.html'
    
class AboutListView(ListView):
    model = Post
    template_name='about.html'
    


class PostListView(ListView):
    model = Post
    template_name='post_list.html'
    context_object_list = 'post_list'
    paginate_by = 3
    
    def get_queryset(self):
        query = self.request.GET.get('title')
        if query:
            return self.model.objects.filter(activate_post=True,title__icontains=query)
        else:
            return self.model.objects.filter(activate_post=True)

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    # success_url = reverse_lazy('post-list')
    
    def form_valid(self, form): 
        user_id = MyUser.objects.filter(email=self.request.user)  
        form = self.get_form()  
        form_model = form.save(commit=False) 
        form_model.user = user_id[0] 
        self.object = form.save()  
        return super(PostCreateView, self).form_valid(form)
    
    
    def get_success_url(self):
         messages.success(self.request, 'Atividade criada com sucesso.')
         return reverse_lazy('post-list')
     

class PostDetailView(DetailView):
     model = Post
     template_name = 'post_detail.html'
     
     def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk) 
        comments = PostComment.objects.filter(post=post).order_by('-created')  
        context = {
            'post': post, 
            'comments':comments,
            'comments_count': comments.count
        }  
        return render(request, 'post_detail.html', context)
    
     def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = PostCommentForm(request.POST) 
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user # user authenticated
            new_comment.post = post
            new_comment.save()
            messages.success(self.request, 'Um novo Comentário foi adicionado com sucesso')
        comments = PostComment.objects.filter(post=post).order_by('-created')

        context = {
            'post': post,
            'form': form,
            'comments':comments
        }

        return render(request, 'post_detail.html', context) 
     

class PostUpdateView(UpdateView):
     model = Post
     template_name = 'post_update.html'
     form_class = PostForm
     success_url = reverse_lazy('post-list')
     
     def get_queryset(self, *args, **kwargs):
         return super().get_queryset(*args, **kwargs).filter(
             user__email=self.request.user
         )
         
     def get_success_url(self):
         messages.success(self.request, 'Atividade atualizada com sucesso.')
         return reverse_lazy('post-detail', args=[self.object.pk])
     
    
    
class PostDeleteView(BaseAdminUserCo,LoginRequiredMixin,DeleteView):
     model = Post
     template_name = 'post_delete.html'
     success_url = reverse_lazy('post-list')
     
     def get_queryset(self, *args, **kwargs):
         return super().get_queryset(*args, **kwargs).filter(
             user__email=self.request.user
         )
    
     def get_success_url(self):
         messages.success(self.request, 'Atividade excluida com sucesso.')
         return reverse_lazy('post-list')
        
     
class CommentEditView(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = PostComment
    fields = ['comment']
    template_name = 'post_detail.html'
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        messages.warning(self.request, 'Comentário atualizado com sucesso')
        return reverse_lazy('post-detail', kwargs={'pk':pk})
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model=PostComment
    template_name="post_detail.html"
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        messages.warning(self.request, 'Comentário deletado com sucesso')
        return reverse_lazy('post-detail', kwargs={'pk': pk})

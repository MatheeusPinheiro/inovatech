from django.urls import path
from post import views as tarefa_views

urlpatterns = [
	
 	path('', tarefa_views.InitialListView.as_view(), name='home'),
 	path('about/', tarefa_views.AboutListView.as_view(), name='about'),
 	path('post/', tarefa_views.PostListView.as_view(), name='post-list'),
	path('post-create/',tarefa_views.PostCreateView.as_view(), name='post-create'),
	path('<int:pk>/', tarefa_views.PostDetailView.as_view(), name='post-detail'),
 	path('post-update/<int:pk>/', tarefa_views.PostUpdateView.as_view(), name='post-update'),
 	path('post-delete/<int:pk>/', tarefa_views.PostDeleteView.as_view(), name='post-delete'),
  	path('post/<int:post_pk>/comment/edit/<int:pk>/', tarefa_views.CommentEditView.as_view(), name="comment-edit"),
   	path('post-delete/<int:pk>/', tarefa_views.CommentDeleteView.as_view(), name='post-delete'),
]

from django.urls import path
from perfil import views


urlpatterns = [
	path("<slug:username>/", views.ProfileView.as_view(), name='user-profile'),
  	path('<int:pk>/update/',views.ProfileEditView.as_view(), name="edit-profile"),
]

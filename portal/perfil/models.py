from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="profile")
    image = models.ImageField(upload_to="profile", default='profile/default-user.png' ,blank=True)
    occupation = models.CharField(max_length=150 , blank=True)
    description: models.TextField( blank=True)
    gender = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
		
    def __str__(self): 
        return f'Profile: {self.user.username}'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        
    @receiver(post_save,sender=settings.AUTH_USER_MODEL)
    def create_profile(sender, **kwargs):
        if kwargs.get('created', False):
            Profile.objects.create(user=kwargs['instance'])
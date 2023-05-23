from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings

class Post(models.Model):
		user = models.ForeignKey(get_user_model(), related_name="posts", on_delete=models.CASCADE)
		title = models.CharField("Titulo",max_length=100)
		description = models.TextField("Descricao", max_length=350)
		published_date = models.DateField()
		created_date = models.DateTimeField(default=timezone.now)
		activate_post = models.BooleanField("Publicar Postagem", default=False)
		created_file = models.FileField('Arquivo', upload_to='post')
		
		def __str__(self):
			return "{} - ({})".format(self.title, self.published_date)

class PostComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment_post") 
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+') 
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
        
    @property
    def children(self):
        return PostComment.objects.filter(parent=self).order_by('-created').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False 
    
    def __str__(self):
        return '{} - {}'.format(self.user.username, self.post.title) 

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['id']
		
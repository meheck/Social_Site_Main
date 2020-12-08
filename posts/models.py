from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
# Create your models here.
import misaka

User=get_user_model()

class Post(models.Model):

     
    user=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    message=models.TextField()
    message_html=models.TextField(editable=False)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username,'pk':self.pk})

    class Meta:
        ordering =['-created_at']
        unique_together=['user','message']
    

class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    create_date=models.DateTimeField(auto_now=True)
    post=models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)

    def __str__(self):
        return self.author
from django.db import models
from django.contrib import auth
from django.contrib.auth import get_user_model

# Create your models here.

UserModel = get_user_model()

class User(auth.models.User,auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)

class Profile(models.Model):
    
    GENDER_OPTIONS = [
        ('ML','MALE'),
        ('FM','FEMALE'),
        ('OT','OTHER'),
    ]
    user = models.ForeignKey(auth.models.User,related_name='profile',on_delete=models.CASCADE,null=True,blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_OPTIONS)
    contact = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='images/',default='images/default.png',null=True,blank=True)
    #followers = models.ManyToManyField("self",symmetrical=False,related_name="following")
    def __str__(self):
       return self.user.username
    
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name="followers")

    def get_follow_instances(self):
        return self.followers.all()

    def get_follow_url(self):
        return reverse("accounts:follow_toggle", kwargs={"slug": self.slug})

    #@property
    #def get_instance_centent_type(self):
        #return ContentType.objects.get_for_model(self.__class__)
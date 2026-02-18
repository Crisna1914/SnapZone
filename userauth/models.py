from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime


# Create your models here.
class Profile(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    # id_user = models.IntegerField(primary_key=True,default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True,default='')
    profileimg = models.ImageField(upload_to='profile_images',default='fstimg.webp')
    location = models.CharField(max_length=100,blank=True,default='')

    def __str__(self):
        return self.user.username
    


class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.CharField( max_length=100)
    image = models.ImageField( upload_to='post_images')
    caption = models.TextField() 
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField( max_length=100)
    def __str__(self):
        return self.username
     

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Followers(models.Model):
    user = models.CharField(max_length=100)
    followers = models.CharField(max_length=100)





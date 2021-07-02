from django.db import models
from datetime import datetime
from datetime import date
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db.models.fields.related import ManyToManyField


######from django.utils import timezone
# Create your models here.

class Certificate(models.Model):
    img = models.ImageField(upload_to="image")

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    friends = ManyToManyField("Profile")

    def __str__(self):
        return self.user.username

class Image(models.Model):
    photo = models.ImageField(upload_to="myimage")
    date = models.DateTimeField(default=datetime.now)
    name = models.ForeignKey(User, on_delete=models.CASCADE)

class Coment(models.Model):
    #id
    message = models.TextField('Message')
    date_comment = models.DateField(default=date.today)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Image, on_delete=models.CASCADE)

class FriendList(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	friends	= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")
    
    #def __str__(self):
    #    return self.user.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.CASCADE)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

class Prediator(models.Model):
    message = models.TextField('Message')
    date_comment = models.DateField(default=date.today)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Image, on_delete=models.CASCADE)

class ImagePre(models.Model):
    photo = models.ImageField(upload_to="myimage")
    date = models.DateTimeField(default=datetime.now)
    name = models.ForeignKey(User, on_delete=models.CASCADE)

class UserStatus(models.Model):
    status = models.ForeignKey(User, on_delete=models.CASCADE)
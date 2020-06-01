from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    # add new to same User class add attribute extending the class no direct inheritinig
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    #additional class to be added
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to= 'profile_pics' , blank =True)
    # there is a folder present in media named profile_pics

    # profile_pic sholud be under media (folder)
    def __str__(self):
        return self.user.username

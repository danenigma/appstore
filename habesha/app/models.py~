from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

	user    = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	
	# Override the __unicode__() method to return out something meaningful!

class AppProfile(models.Model):

	user      =  models.ForeignKey(User)
	name      =  models.CharField(max_length = 100)
	pub_date  =  models.DateField(auto_now_add = True)
	catagory  =  models.CharField(max_length = 100)
	apk       =  models.FileField(upload_to = 'apks',blank = True)
	screen_shot = models.ImageField(upload_to ='screenshots',blank = True)
	down_number = models.IntegerField(default = 0)	
	rating    =  models.IntegerField(default  = 0)
	comments  =  models.TextField(blank = True)
	discription = models.TextField(blank = True)

class AppStatus(models.Model):
	#app       =  models.OneToOneField(AppProfile) 
	down_number = models.IntegerField(blank =True)	
	rating    =  models.IntegerField(blank  = True)






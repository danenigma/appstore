from django.shortcuts import render,render_to_response
from django.template import RequestContext, loader
# Create your views here.
from .forms import UserForm, UserProfileForm,AppForm
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import AppProfile,AppStatus
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Use the login_required() decorator to ensure only those logged in can access the view.7

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/home')

@login_required
def upload(request):
	context = RequestContext(request)
	upload_done = False
	if request.method == 'POST':
		app_form = AppForm(data=request.POST)
		
	
		if app_form.is_valid():
			uploader  = User.objects.get(username = request.user)
		
			app = app_form.save(commit=False)
			app.user = uploader
			if 'screen_shot' in request.FILES:
				
				app.screen_shot = request.FILES['screen_shot']

		        if 'apk' in request.FILES:
				
				app.apk = request.FILES['apk']
					
			app.save()
			
                        upload_done = True
			print upload_done
		else:
			print app_form.errors
	else:
		app_form = AppForm()
		
	return render_to_response('upload.html',{'app_form': app_form,  'upload_done':upload_done},context)

def register(request):
# Like before, get the request's context.
	context = RequestContext(request)
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
	
		if user_form.is_valid() and profile_form.is_valid():
		
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				
				profile.picture = request.FILES['picture']
			
			profile.save()
                        registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
# Render the template depending on the context.
	return render_to_response('register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered':registered},context)

def home(request):

	users = User.objects.all()
	apps  = AppProfile.objects.all()
	MEDIA_URL = '/media/'
	cat = 'all'
        return render(request,'index.html',{'users':users,'MEDIA_URL' : MEDIA_URL,'apps':apps,'cat':cat})        
def games(request):
	MEDIA_URL = '/media/'	
	apps = AppProfile.objects.filter(catagory = "game")
	cat = 'game'
        return render(request,'index.html',{'MEDIA_URL' : MEDIA_URL,'apps':apps,'cat':cat})
def educational(request):
	MEDIA_URL = '/media/'	
	apps = AppProfile.objects.filter(catagory = "educational")
	cat = 'educational'
        return render(request,'index.html',{'MEDIA_URL' : MEDIA_URL,'apps':apps,'cat':cat})
	
def topchart(request):
	MEDIA_URL = '/media/'
	apps  = AppProfile.objects.order_by('down_number')[:3]
	cat = 'all'
        return render(request,'index.html',{'MEDIA_URL' : MEDIA_URL,'apps':apps,'cat':cat})
def down(request,app):
	 
	MEDIA_URL = '/media/'
	app = AppProfile.objects.get(id = app)
	d = app.down_number
	app.down_number  = d+1
	app.save()
        return render(request,'download.html',{'MEDIA_URL' : MEDIA_URL,'app':app})
	
def rating(request,app,rate):
	app = AppProfile.objects.get(id = app)
	MEDIA_URL = '/media/'
	d = app.rating
	app.rating  = d+ int(rate)
	app.save()
        return render(request,'download.html',{'MEDIA_URL' : MEDIA_URL,'app':app})
def newreleases(request):
	MEDIA_URL = '/media/'
	apps  = AppProfile.objects.order_by('pub_date')[:3]
	cat = 'all'
        return render(request,'index.html',{'MEDIA_URL' : MEDIA_URL,'apps':apps,'cat':cat})


def search(request):
	if request.method == 'POST':
		MEDIA_URL = '/media/'
		value  = str(request.POST['item'])
		print value
		apps = AppProfile.objects.filter(name__contains = value)
		print apps
		cat  = "all"
		return render(request,'search.html',{'MEDIA_URL' : MEDIA_URL,'apps':apps,'cat' :cat})		

		
@login_required
def developer(request):
	
	user = User.objects.get(username = request.user) 
	MEDIA_URL = '/media/'
	apps = AppProfile.objects.all()
	new_apps = []
	for app in apps:
		if app.user == user:
			new_apps.append(app)
        return render(request,'developer.html',{'user':user,'MEDIA_URL' : MEDIA_URL,'apps':new_apps})
	

def user_login(request):
	# Like before, obtain the context for the user's request.
	context = RequestContext(request)
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
	# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
	  	if user is not None:
			# Is the account active? It could have been disabled.
			if user.is_active:
				login(request, user)
				print "wassupp!"
			
				return HttpResponseRedirect('/dev/')
			else:
			
				return HttpResponse("Your Rango account is disabled.")
		else:

			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	else:
		print "he"
		return render(request,'signin.html',{})



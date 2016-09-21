from django.shortcuts import render, HttpResponse, redirect
from .models import Users
from django.contrib import messages

def index(request):
	return render(request, "log/index.html")



def login(request):


	return render(request, "log/login.html")

def log(request):
	res = Users.objects.login(request.POST)
	if res ["created"]:
		register = res["created"]
		messages.success(request, "Success!")

	else:
		for error in res["errors"]:
			messages.error(request, error)
			return redirect ('/login')
	
	return redirect ('/success')


def process(request):
	if request.method == "POST":

		res = Users.objects.register(request.POST)
		if res ["created"]:
			register = res["created"]
			messages.success(request, "Sucess!")

		else:
			for error in res["errors"]:
				messages.error(request, error)
				return redirect ('/')
	
	return redirect ('/success')


def success(request):
	user = Users.objects.all()
	context = {'user':user}

	return render(request, "log/success.html", context)

def remove(request, id):

	this = Users.objects.get(id=id)
	if request.method == "GET":
		context = {'user':this}
		return render(request, "log/success.html", context)

	this.delete()	
	return redirect ('/success')
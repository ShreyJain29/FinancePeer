from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout , decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db import IntegrityError
# Create your views here.

def register(request):
    if request.method == "POST":
        first_r = request.POST['first_name']
        last_r = request.POST['last_name']
        email_r = request.POST['email']
        password_r = request.POST['password']
        password2_r = request.POST['confirm_password']
        username_r = request.POST['username']
        if password_r != password2_r:
            return render(request, "FD/signup.html",{
                "message": "Passwords must match.",
            })

        try:
            user = User.objects.create_user(first_name=first_r, last_name=last_r, username=username_r,
                                                email=email_r, password=password_r)


            user.save()
        except IntegrityError:
            return render(request, "FD/signup.html", {
                "message": "Email already exist."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "FD/signup.html")


def loginuser(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            email_p = request.POST['email']
            password_p = request.POST['password']
            user = authenticate(request, username=email_p, password=password_p)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "FD/login.html", {
                    "email": email_p,
                    "flag": True
                })
        return render(request, "FD/login.html")
    else:
        return HttpResponseRedirect(reverse("index"))


def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@decorators.login_required(login_url='/login')
def index(request):

    if request.method == "POST":
        f = request.FILES['file']
        if f.name[-4:] == 'json':
            book = fileupload()
            book.upload = f
            book.save()
            file_parse_update(book)
            return render(request, "FD/file_upload.html", {
                "message": "File uploaded and parsed.  "
            })
        else:
            return render(request, "FD/file_upload.html", {
                "message" : "Only json type file can be uploaded. "
            })



    return render(request, "FD/file_upload.html")



def file_parse_update(f):
    import json
    with open(f.upload.name,'rb') as data_file:
        data = json.load(data_file)


    for i in data:
        temp = Filemodel()
        a = User.objects.get(pk = i['userId'])
        temp.Fuser = a
        temp.Body = i['body']
        temp.Title = i['title']
        temp.save()


def display_data(request):
    return render(request , "FD/displayFD.html",{
        "c" : Filemodel.objects.all()
    })
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime
from django.contrib import messages
from .models import User, Post

class NewPostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all(),
        "form": NewPostForm()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            user = request.user
            timestamp = datetime.now()
            post = Post(user=user, content=content, timestamp=timestamp)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid form")
            return HttpResponseRedirect(reverse("index"))
        

@login_required
def remove_post(request):
    if request.method == "POST":
        post = Post.objects.get(pk=request.POST["post_id"])
        post.delete()
        
        
    
    return HttpResponseRedirect(reverse("index"))
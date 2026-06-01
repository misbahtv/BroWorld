from django.shortcuts import render,redirect
from .forms import RegistrationForm,LoginForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from posts.models import Post,Follow

@login_required
def feed(request):
    posts=Post.objects.select_related('user').order_by('-created_at')
    for post in posts:
        post.user_liked=post.likes.filter(user=request.user).exists()
        post.user_following_author=Follow.objects.filter(follower=request.user,following=post.user).exists()
        post.user_to_follow=post.user
    return render(request,'accounts/feed.html',{'posts':posts})

def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:feed')
    if request.method=='POST':
        form=RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('accounts:feed')
    else:
        form=RegistrationForm()
    return render(request,'accounts/register.html',{'form':form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:feed')
    if request.method=='POST':
        form=LoginForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('accounts:feed')
    else:
        form=LoginForm(request)
    return render(request,'accounts/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('accounts:login')
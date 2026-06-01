from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,LoginForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from posts.models import Post,Follow
from django.contrib.auth import get_user_model

User=get_user_model()

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

@login_required
def profile_user(request,user_id):
    profile_user=get_object_or_404(User,id=user_id)     
    posts=profile_user.posts.order_by('-created_at')
    followers_count=Follow.objects.filter(following=profile_user).count()
    following_count=Follow.objects.filter(follower=profile_user).count()
    user_following_profile_user=False
    if Follow.objects.filter(follower=request.user,following=profile_user).exists():
        user_following_profile_user=True
    return render(request,'accounts/profile.html',{'profile_user': profile_user,
                                                'posts': posts,
                                                "followers_count":followers_count,
                                                "following_count":following_count,
                                                "user_following_author":user_following_profile_user,
                                                "user_to_follow": profile_user
                                                }
                                            )
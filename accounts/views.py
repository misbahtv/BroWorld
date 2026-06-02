from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,LoginForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from posts.models import Post,Follow
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User=get_user_model()

@login_required
def feed(request):
    posts=Post.objects.select_related('user').order_by('-created_at')
    for post in posts:
        post.user_liked=post.likes.filter(user=request.user).exists()
        post.like_count=post.likes.count()
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
                                                "user_to_follow": profile_user,
                                                'source':'profile'
                                                }
                                            )


@login_required
def edit_profile(request):
    if request.method=='POST':
        form=UserUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile',user_id=request.user.id)
    else:
        form=UserUpdateForm(instance=request.user)
    return render(request,'accounts/edit_profile.html',{'form':form})


@login_required
def followers_list(request,user_id):
    profile_user=get_object_or_404(User,id=user_id)
    followers=Follow.objects.select_related('follower').filter(following=profile_user)
    return render(request,'accounts/followers_list.html',{'profile_user': profile_user,'followers': followers})

@login_required
def following_list(request,user_id):
    profile_user=get_object_or_404(User,id=user_id)
    following=Follow.objects.select_related('following').filter(follower=profile_user)
    return render(request,'accounts/following_list.html',{'profile_user': profile_user,'following': following})


@login_required
def user_search(request):
    query = request.GET.get('q', '')
    users = User.objects.none()

    if query:
        users = User.objects.filter(
            username__icontains=query).exclude(id=request.user.id)
        following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id',flat=True))

        for user in users:
            user.user_following_author = (user.id in following_ids)

    context = {
        'users': users,
        'query': query,
    }

    if request.htmx:
        return render(request,'accounts/partials/search_results.html',context)

    return render(request,'accounts/search.html',context)
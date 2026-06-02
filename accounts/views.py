from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,LoginForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from posts.models import Post,Follow,Like
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.core.paginator import Paginator

User=get_user_model()

@login_required
def feed(request):
    following_ids = set(
        Follow.objects.filter(
            follower=request.user
        ).values_list(
            'following_id',
            flat=True
        )
    )

    liked_post_ids = set(
        Like.objects.filter(
            user=request.user
        ).values_list(
            'post_id',
            flat=True
        )
    )

    posts = (
        Post.objects
        .select_related('user')
        .annotate(
            like_count=Count('likes')
        )
        .order_by('-created_at')
    )

    for post in posts:

        post.user_liked = (
            post.id in liked_post_ids
        )

        post.user_following_author = (
            post.user_id in following_ids
        )

        post.user_to_follow = post.user

    paginator=Paginator(posts,10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    if request.htmx:
        return render(
            request,
            'accounts/partials/post_list.html',
            {
                'page_obj': page_obj
            }
        )

    return render(
        request,
        'accounts/feed.html',
        {
            'page_obj': page_obj
        }
    )


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

from django.core.paginator import Paginator

@login_required
def profile_user(request, user_id):
    profile_user = get_object_or_404(User,id=user_id)
    posts = profile_user.posts.order_by('-created_at')
    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    user_following_profile_user = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    paginator = Paginator(posts,9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(
        page_number
    )

    if request.htmx:
        return render(
            request,
            'accounts/partials/profile_post_grid.html',
            {
                'page_obj': page_obj,
            }
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'profile_user': profile_user,
            'page_obj': page_obj,
            'followers_count': followers_count,
            'following_count': following_count,
            'user_following_author': user_following_profile_user,
            'user_to_follow': profile_user,
            'source': 'profile',
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


@login_required
def home(request):
    following_ids = set(Follow.objects.filter(follower=request.user).values_list('following_id',flat=True))
    following_ids.add(request.user.id)
    liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id',flat=True))
    posts = (
        Post.objects
        .select_related('user')
        .filter(
            user_id__in=following_ids
        )
        .annotate(
            like_count=Count('likes')
        )
        .order_by('-created_at')
    )

    for post in posts:
        post.user_liked = (post.id in liked_post_ids)
        post.user_following_author = (post.user_id in following_ids)
        post.user_to_follow = post.user

    paginator=Paginator(posts,10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    if request.htmx:
        return render(
            request,
            'accounts/partials/post_list.html',
            {
                'page_obj': page_obj
            }
        )

    return render(
        request,
        'accounts/home.html',
        {
            'page_obj': page_obj
        }
    )

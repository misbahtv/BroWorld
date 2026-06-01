from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm,CommentForm
from posts.models import Post,Like,Follow
from django.contrib.auth import get_user_model
from django.http import HttpResponse

@login_required
def create_post(request):
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('accounts:feed')
    else:
        form=PostForm()
    return render(request,'posts/create_post.html',{'form':form})

@login_required
def detail_post(request,post_id):
    post=get_object_or_404(Post.objects.select_related('user'),id=post_id)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.user=request.user
            comment.post=post
            comment.save()
            return redirect('posts:detail_post',post_id=post.id)
    else:
        form=CommentForm()
    
    comments=post.comments.select_related('user').order_by('created_at')
    return render(request,'posts/detail_post.html',{'post':post,'comments':comments,'comment_form':form})

@login_required
def toggle_like(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    like=Like.objects.filter(user=request.user,post=post)
    if like.exists():
        like.delete()
        post.user_liked=False
    else:
        Like.objects.create(user=request.user,post=post)
        post.user_liked=True
    return render(request,'posts/partials/like_section.html',{'post':post})

@login_required
def toggle_follow(request, user_id):
    User = get_user_model()
    user_to_follow = get_object_or_404(User,id=user_id)
    if user_to_follow == request.user:
        return HttpResponse(status=400)
    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    )
    if follow.exists():
        follow.delete()
        user_following_author = False
    else:
        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )
        user_following_author = True
    return render(
        request,
        'posts/partials/follow_section.html',
        {
            'user_to_follow': user_to_follow,
            'user_following_author': user_following_author,
        }
    )
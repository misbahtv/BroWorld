from django.db import models
from django.conf import settings

class Post(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
                           )
    content=models.TextField()
    image=models.ImageField(upload_to='posts/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.id}"
    

class Comment(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.id}"
    

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_like'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.post.id}"


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
        )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
        )
    created_at = models.DateTimeField(
        auto_now_add=True
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow_relationship'
                ),
            models.CheckConstraint(
                condition=~models.Q(
                    follower=models.F('following')
                    ),
                name='prevent_self_follow'
                )
            ]
        
    def __str__(self):
        return f"{self.follower.username} is following {self.following.username}"
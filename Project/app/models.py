from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.conf import settings
from django.utils import timezone

def get_default_imatge():
    return settings.DEFAULT_AVATAR


# Create your models here.
class User(AbstractUser):
    #camps personalitzats
    bio = models.TextField(blank=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/',default=get_default_imatge(), null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.username}"

    @property
    def estadistiques(self):
        return {
            'num_publicacions': len(self.publications.all()),
            'num_comentaris': len(self.comments.all())
        }



class Community(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    id = models.CharField(max_length=20, primary_key=True)
    banner = models.ImageField(upload_to='communitiesPictures/', blank=True, null=True)
    avatar = models.ImageField(upload_to='communitiesPictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def subs(self):
        return Subscription.objects.filter(community_sub=self).count()

    @property
    def publi(self):
        return Post.objects.filter(community=self).count()

    @property
    def comments(self):
        p = Post.objects.filter(community=self)
        count = 0
        for post in p:
            count += Comments.objects.filter(post=post).count()
        return count


class Post(models.Model):
    url = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True, related_name="community")
    poster = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    created_at = models.DateTimeField(default=datetime.now)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)
    numComments = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Poster: {self.poster}, title: {self.title}"

    @property
    def resta(self):
        return self.positive - self.negative


class Comments(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comentor")
    content = models.CharField(max_length=500)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="post")
    editing = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f"Content {self.content} votes {self.positive - self.negative}"

    @property
    def resta(self):
        return self.positive - self.negative


class Votes(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="voter")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="postComented")
    type = models.CharField(max_length=8, default=None)

    class Meta:
        unique_together = ('voter', 'post')

    def __str__(self):
        return f"${self.voter} voted this post: ${self.post} in ${self.type} way"


class VotesComments(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="voterC")
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, blank=True, null=True, related_name="commentVoted")
    type = models.CharField(max_length=8, default=None)


class Like(models.Model):
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_like")
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="post_liked")

    def __str__(self):
        return f"User ${self.user_like} liked this post ${self.post_liked}"


class LikeComment(models.Model):
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userC_like")
    comment_liked = models.ForeignKey(Comments, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name="comment_liked")

class Comment(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

class Subscription(models.Model):
    user_sub = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_sub")
    community_sub = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True, related_name="community_sub")


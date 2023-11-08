from django.contrib import admin
from .models import User, Community, Post, Comments, Votes, Like, Comment, Subscription, VotesComments, LikeComment

# Register your models here.
admin.site.register(User)
admin.site.register(Community)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Votes)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Subscription)
admin.site.register(VotesComments)
admin.site.register(LikeComment)
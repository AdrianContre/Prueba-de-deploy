from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("createPost", views.createPost, name="createPost"),
    path("userProfile/<str:username>/", views.view_userProfile, name="userProfile"),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("social-auth/", include('social_django.urls', namespace="social")),
    path('userProfile/<str:username>/edit/', views.edit_userProfile, name='edit_user_profile'),
    path("post/<int:postId>", views.post, name="post"),
    path("comment/<int:postId>", views.comment, name="comment"),
    path("vote/<int:postId>/<str:typeV>", views.vote, name="vote"),
    path("like/<int:postId>", views.like, name="like"),
    path("delete/<int:postId>", views.delete, name="delete"),
    path("edit/<int:postId>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path('process_text/', views.process_text, name='process_text'),
    path('proccess_comentaris/', views.proccess_comentaris, name='proccess_comentaris'),
    path("createCommunity",views.createCommunity,name="createCommunity"),
    path("listCommunity", views.listCommunity, name="listCommunity"),
    path("subscribeCommunity/<str:community_name>", views.subscribeCommunity, name="subscribeCommunity"),

    path("editComment/<int:commentId>",views.editComment,name="editComment"),
    path("deleteComment/<int:commentId>",views.deleteComment,name="deleteComment"),
    path("voteComment/<int:commentId>/<str:typeV>", views.voteComment,name="voteComment"),
    path("cancelEdit/<int:commentId>",views.cancelEdit,name="cancelEdit"),
    path("likeComment/<int:commentId>",views.likeComment,name="likeComment"),
    path("replyComment/<int:commentId>",views.replyComment,name="replyComment"),
    path("voteInPosts/<int:postId>/<str:typeV>",views.voteInPosts,name="voteInPosts"),
    path("likeInPosts/<int:postId>",views.likeInPosts,name="likeInPosts"),
    path("voteInProfile/<int:postId>/<str:typeV>/<str:username>",views.voteInProfile,name="voteInProfile"),
    path("likeInProfile/<int:postId>/<str:username>",views.likeInProfile,name="likeInProfile"),
]
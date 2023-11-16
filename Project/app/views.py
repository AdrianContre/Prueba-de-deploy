from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import MyForm
from .forms import CercaForm
from .forms import TextForm
from .forms import TextComForm
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import User,Community,Post,Comments,Votes,Like,VotesComments,LikeComment,Subscription, Comment
from collections import OrderedDict
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
import numpy as np


WhatShow = "Publicacions"

def infopost(ordPost, request):
    infoPosts = []
    for p in ordPost:
        u = request.user
        v = 'caca'
        try:
            b = Votes.objects.get(voter=u, post=p)
            v = b.type
            b = True
        except:
            b = False
            v = None

        try:
            l = Like.objects.get(user_like=u, post_liked=p)
            liked = True
        except:
            liked = False
        infoPosts.append((p, b, v, liked))

    return infoPosts

def InfoComments(comments, request):
    u = request.user
    array_comments = []
    for c in comments:
        voted = None
        t = None
        lik = None
        try:
            vc = VotesComments.objects.get(voter=u, comment=c)
            voted = True
            t = vc.type
        except:
            voted = False
            t = None
        try:
            lc = LikeComment.objects.get(user_like=u, comment_liked=c)
            lik = True
        except:
            lik = False
        array_comments.append((c, voted, t, lik))

    return array_comments

def index(request):
    global WhatShow
    user = request.user
    button = request.GET.get('button')
    button2 = request.GET.get('button2')
    if button2 is not None: WhatShow = button2
    if WhatShow == "Publicacions":
        if button is None or button == 'Tot':
            ordPost = Post.objects.all().order_by('-created_at')
            form = MyForm(request.POST)
            if request.method == 'POST':
                form = MyForm(request.POST)
                selected_option = form.data['order']
                if selected_option == 'New':
                    ordPost = Post.objects.all().order_by('-created_at')
                elif selected_option == 'Old':
                    ordPost = Post.objects.all().order_by('created_at')
                elif selected_option == 'Most comments':
                    comments = OrderedDict()
                    for p in Post.objects.all():
                        comments[p] = p.numComments
                    comments = OrderedDict(sorted(comments.items(), key=lambda item: item[1], reverse=True))
                    ordPost = list(comments.keys())
                elif selected_option == 'The best(El NANO)':
                    votes = OrderedDict()
                    for p in Post.objects.all():
                        votes[p] = p.resta
                    votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
                    ordPost = list(votes.keys())
            else:
                form = MyForm()

            ordPostI = infopost(ordPost, request)
            p_c = True
            return render(request, "app/posts.html", {"posts": ordPostI,"form": form, "p_c": p_c, "comments": ordPostI})

        else:
            if button == 'Subscrit' and not user.is_authenticated:
                return render(request, template_name="app/login.html")
            else:
                sub = Subscription.objects.filter(user_sub=user)
                if button == 'Subscrit':
                    if len(sub) == 0:
                        form = MyForm()
                        return render(request, "app/posts.html", {"posts": [],"form": form, "p_c": True, "comments": []})
                    v = []
                    for s in sub:
                        v.append(Post.objects.filter(community=s.community_sub))
                    l = np.concatenate(v)
                    ordPost = sorted(l, key=lambda x: x.created_at, reverse=True)
                    form = MyForm(request.POST)
                    if request.method == 'POST':
                        form = MyForm(request.POST)
                        selected_option = form.data['order']
                        if selected_option == 'New':
                            ordPost = sorted(l, key=lambda x: x.created_at, reverse=True)
                        elif selected_option == 'Old':
                            ordPost = sorted(l, key=lambda x: x.created_at, reverse=False)
                        elif selected_option == 'Most comments':
                            comments = OrderedDict()
                            for p in l:
                                comments[p] = p.numComments
                            comments = OrderedDict(sorted(comments.items(), key=lambda item: item[1], reverse=True))
                            ordPost = list(comments.keys())
                        elif selected_option == 'The best(El NANO)':
                            votes = OrderedDict()
                            for p in l:
                                votes[p] = p.resta
                            votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
                            ordPost = list(votes.keys())

                        ordPostI = infopost(ordPost, request)
                        p_c = True
                        return render(request, "app/posts.html", {"posts": ordPostI, "form": form, "p_c": p_c, "comments": ordPostI})

                    else:
                        form = MyForm()

                    ordPostI = infopost(ordPost, request)
                    p_c = True
                    return render(request, "app/posts.html", {"posts": ordPostI, "form": form, "p_c": p_c, "comments": ordPostI})

    elif WhatShow == 'Comments':
        if button is None or button == 'Tot':
            ordComments = Comments.objects.all().order_by('-created_at')
            form = MyForm(request.POST)
            if request.method == 'POST':
                form = MyForm(request.POST)
                selected_option = form.data['order']
                if selected_option == 'New':
                    ordComments = Comments.objects.all().order_by('-created_at')
                elif selected_option == 'Old':
                    ordComments = Comments.objects.all().order_by('created_at')
                elif selected_option == 'Most comments':
                    commentsPost = OrderedDict()
                    for p in Post.objects.all():
                        for c in Comments.objects.all():
                            if c.post == p: #por cada comentario miramos si pertenece al post
                                commentsPost[c] = len(c.replies.all())
                    OrdComments = OrderedDict(sorted(commentsPost.items(), key=lambda item: item[1], reverse=True))
                    ordComments = list(OrdComments.keys())
                elif selected_option == 'The best(El NANO)':
                    votes = OrderedDict()
                    for c in Comments.objects.all():
                        votes[c] = c.resta
                    votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
                    ordComments = list(votes.keys())
            else:
                form = MyForm()

            ordCommentsI = InfoComments(ordComments, request)
            p_c = False
            return render(request, "app/posts.html",
                          {"post": ordCommentsI, "form": form, "p_c": p_c, "comments": ordCommentsI})

        else:
            if button == 'Subscrit' and not user.is_authenticated:
                return render(request, template_name="app/login.html")
            else:
                sub = Subscription.objects.filter(user_sub=user)
                if button == 'Subscrit':
                    if len(sub) == 0:
                        form = MyForm()
                        return render(request, "app/posts.html", {"posts": [],"form": form, "p_c": False, "comments": []})
                    v = []
                    for s in sub:
                        v.append(Post.objects.filter(community=s.community_sub))
                    l = np.concatenate(v)
                    c = []
                    for p in l:
                        c.append(Comments.objects.filter(post=p))
                    l = np.concatenate(c)
                    ordComments = sorted(l, key=lambda x: x.created_at, reverse=True)
                    form = MyForm(request.POST)
                    if request.method == 'POST':
                        form = MyForm(request.POST)
                        selected_option = form.data['order']
                        if selected_option == 'New':
                            ordComments = sorted(l, key=lambda x: x.created_at, reverse=True)
                        elif selected_option == 'Old':
                            ordComments = sorted(l, key=lambda x: x.created_at, reverse=False)
                        elif selected_option == 'Most comments':
                            comments = OrderedDict()
                            for p in l:
                                comments[p] = p.numComments
                            comments = OrderedDict(sorted(comments.items(), key=lambda item: item[1], reverse=True))
                            ordComments = list(comments.keys())
                        elif selected_option == 'The best(El NANO)':
                            votes = OrderedDict()
                            for p in l:
                                votes[p] = p.resta
                            votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
                            ordComments = list(votes.keys())

                        ordCommentsI = InfoComments(ordComments, request)
                        p_c = False
                        return render(request, "app/posts.html",{"posts": ordCommentsI, "form": form, "p_c": p_c, "comments": ordCommentsI})

                    else:
                        form = MyForm()

                    ordCommentsI = InfoComments(ordComments, request)
                    p_c = False
                    return render(request, "app/posts.html", {"posts": ordCommentsI, "form": form, "p_c": p_c, "comments": ordCommentsI})

    else:
        form = MyForm()
        ordPost = Post.objects.all().order_by('-created_at')
        ordPostI = infopost(ordPost, request)
        p_c = True
        return render(request, "app/posts.html", {"posts": ordPostI, "form": form, "p_c": p_c, "comments": ordPostI})

def view_userProfile(request, username):
    try:
        button = request.GET.get('button', 'Publicaciones')  # Por defecto a 'Publicaciones'

        if button == "Publicaciones":
            user_profile = User.objects.get(username=username)
            if request.method == "POST":
                form = MyForm(request.POST)
                selected_option = form.data['order']
            else:
                form = MyForm()
                selected_option = 'New'

            if selected_option == 'New':
                ordPost = Post.objects.filter(poster=user_profile).order_by('-created_at')
            elif selected_option == 'Old':
                ordPost = Post.objects.filter(poster=user_profile).order_by('created_at')
            elif selected_option == 'Most comments':
                comments = OrderedDict()
                for p in Post.objects.filter(poster=user_profile):
                    comments[p] = p.numComments
                comments = OrderedDict(sorted(comments.items(), key=lambda item: item[1], reverse=True))
                ordPost = list(comments.keys())
            elif selected_option == 'The best(El NANO)':
                votes = OrderedDict()
                for p in Post.objects.filter(poster=user_profile):
                    votes[p] = p.resta
                votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
                ordPost = list(votes.keys())

            ordPostI = infopost(ordPost, request)
            array_comments = []
            liked_posts_info = []
            liked_comments_info = []

            return render(request, 'app/userProfile.html', {
                'user_profile': user_profile,
                'user_posts': ordPostI,
                'user_comments': array_comments,
                'button': button,
                'like_posts': liked_posts_info,
                'like_comments': liked_comments_info,
                'form': form
            })

        elif button == "Comentarios":
            user_profile = User.objects.get(username=username)
            if request.method == "POST":
                form = MyForm(request.POST)
                selected_option = form.data['order']
            else:
                form = MyForm()
                selected_option = 'New'

            if selected_option == 'New':
                array_comments = Comments.objects.filter(commentor=user_profile).order_by('-created_at')
            elif selected_option == 'Old':
                array_comments = Comments.objects.filter(commentor=user_profile).order_by('created_at')
            elif selected_option == 'Most comments':
                commentsPost = OrderedDict()
                for p in Post.objects.filter(poster=user_profile):
                    for c in Comments.objects.filter(commentor=user_profile):
                        if c.post == p:  # por cada comentario miramos si pertenece al post
                            commentsPost[c] = len(c.replies.all())
                OrdComments = OrderedDict(sorted(commentsPost.items(), key=lambda item: item[1], reverse=True))
                array_comments = list(OrdComments.keys())
            elif selected_option == 'The best(El NANO)':
                votes = OrderedDict()
                for c in Comments.objects.all():
                    votes[c] = c.resta
                votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
                array_comments = list(votes.keys())

            ordPostI = []
            liked_posts_info = []
            liked_comments_info = []
            array_comments = InfoComments(array_comments, request)

            return render(request, 'app/userProfile.html', {
                'user_profile': user_profile,
                'user_posts': ordPostI,
                'user_comments': array_comments,
                'button': button,
                'like_posts': liked_posts_info,
                'like_comments': liked_comments_info,
                'form': form
            })

        else:
            user_profile = User.objects.get(username=username)
            user_posts = Post.objects.filter(poster=user_profile).order_by('-created_at')
            user_comments = Comments.objects.filter(commentor=user_profile)
            liked_posts = Like.objects.filter(user_like=user_profile)
            liked_comments = LikeComment.objects.filter(user_like=user_profile)
            form = MyForm(request.POST)
            infoPosts = []
            for p in user_posts:
                u = request.user
                v = 'caca'
                try:
                    b = Votes.objects.get(voter=u, post=p)
                    v = b.type
                    b = True
                except:
                    b = False
                    v = None

                try:
                    l = Like.objects.get(user_like=u, post_liked=p)
                    liked = True
                except:
                    liked = False
                infoPosts.append((p, b, v, liked))

            array_comments = []
            for c in user_comments:
                u = request.user
                voted = None
                t = None
                lik = None
                try:
                    vc = VotesComments.objects.get(voter=u, comment=c)
                    voted = True
                    t = vc.type
                except:
                    voted = False
                    t = None
                try:
                    lc = LikeComment.objects.get(user_like=u, comment_liked=c)
                    lik = True
                except:
                    lik = False
                array_comments.append((c, voted, t, lik))

            # desats
            liked_posts_info = []
            for p in liked_posts:
                print(p)
                u = request.user
                v = 'caca'
                try:
                    b = Votes.objects.get(voter=u, post=p.post_liked)
                    v = b.type
                    b = True
                except:
                    b = False
                    v = None

                liked_posts_info.append((p.post_liked, b, v, True))

            liked_comments_info = []
            for c in liked_comments:
                print(c)
                u = request.user
                voted = None
                t = None
                try:
                    vc = VotesComments.objects.get(voter=u, comment=c.comment_liked)
                    voted = True
                    t = vc.type
                except:
                    voted = False
                    t = None

                liked_comments_info.append((c.comment_liked, voted, t, True))

            ordPostI = []
            array_comments = []

            if request.method == "POST":
                form = MyForm(request.POST)
                selected_option = form.data['order']
            else:
                form = MyForm()
                selected_option = 'New'

            if selected_option == 'New':
                i = 0
                for c in liked_comments_info:
                    liked_comments_info[i] = (c[0], c[1], c[2], True, c[0].created_at)
                    i += 1
                liked_comments_info = sorted(liked_comments_info, key=lambda x: x[4], reverse=True)
                i = 0
                for p in liked_posts_info:
                    liked_posts_info[i] = (p[0], p[1], p[2], True, p[0].created_at)
                    i += 1
                liked_posts_info = sorted(liked_posts_info, key=lambda x: x[4], reverse=True)

            elif selected_option == 'Old':
                i = 0
                for c in liked_comments_info:
                    liked_comments_info[i] = (c[0], c[1], c[2], True, c[0].created_at)
                    i += 1
                liked_comments_info = sorted(liked_comments_info, key=lambda x: x[4])
                i = 0
                for p in liked_posts_info:
                    liked_posts_info[i] = (p[0], p[1], p[2], True, p[0].created_at)
                    i += 1
                liked_posts_info = sorted(liked_posts_info, key=lambda x: x[4])

            elif selected_option == 'Most comments':
                #comments
                commentsPost = OrderedDict()
                for c in liked_comments_info:
                    for p in Post.objects.all():
                        if c[0].post == p:
                            commentsPost[c] = len(c[0].replies.all())
                OrdComments = OrderedDict(sorted(commentsPost.items(), key=lambda item: item[1], reverse=True))
                liked_comments_info = list(OrdComments.keys())
                #posts
                comments = OrderedDict()
                for p in liked_posts_info:
                    comments[p] = p[0].numComments
                comments = OrderedDict(sorted(comments.items(), key=lambda item: item[1], reverse=True))
                liked_posts_info = list(comments.keys())


            elif selected_option == 'The best(El NANO)':
                i = 0
                for c in liked_comments_info:
                    liked_comments_info[i] = (c[0], c[1], c[2], True, c[0].resta)
                    i += 1
                liked_comments_info = sorted(liked_comments_info, key=lambda x: x[4], reverse = True)
                i = 0
                for p in liked_posts_info:
                    liked_posts_info[i] = (p[0], p[1], p[2], True, p[0].resta)
                    i += 1
                liked_posts_info = sorted(liked_posts_info, key=lambda x: x[4], reverse =True)

            return render(request, 'app/userProfile.html', {
                'user_profile': user_profile,
                'user_posts': ordPostI,
                'user_comments': array_comments,
                'button': button,
                'like_posts': liked_posts_info,
                'like_comments': liked_comments_info,
                'form': form
            })

    except User.DoesNotExist:
        raise Http404("El usuario no existe")


def login(request):
    return render(request,'app/login.html')


def process_text(request):
    if request.method == 'POST':
        formName = request.POST.get('name')
        if formName == "tipusCerca":
            formC = CercaForm(request.POST)
            order_value = formC.data['order']
            if order_value == 'cercapub':
                formText = TextForm(request.POST)
                return render(request, 'app/cercadorPublicacions.html', {"form": formText, "cercaForm": formC})
            if order_value == 'cercacom':
                formText = TextComForm(request.POST)
                return render(request, 'app/cercadorComentaris.html', {"form": formText, "cercaForm": formC})
        else:
            matching_posts = []
            form = TextForm(request.POST)
            for p in Post.objects.all():
                if form.data['text_input'] in p.title:
                    matching_posts.append(p)
            if matching_posts:
                formC = CercaForm(request.POST)
                formText = TextForm(request.POST)
                return render(request, "app/cercadorPublicacionsMatch.html", {"posts": matching_posts, "cercaForm": formC, "form": formText})
            else:
                formCerca = CercaForm(request.POST)
                return render(request, "app/cercadorPublicacionsNoMatch.html", {"form": form, "cercaForm": formCerca})
    else:
        form = TextForm()

    return render(request, 'app/layout.html')


def proccess_comentaris(request):
    if request.method == 'POST':
        formName = request.POST.get('name')
        if formName == "tipusCerca":
            formC = CercaForm(request.POST)
            order_value = formC.data['order']
            if order_value == 'cercapub':
                formText = TextForm(request.POST)
                return render(request, 'app/cercadorPublicacionsMatch.html', {"form": formText, "cercaForm": formC})
            if order_value == 'cercacom':
                formText = TextComForm(request.POST)
                return render(request, 'app/cercadorComentaris.html', {"form": formText, "cercaForm": formC})
        else:
            matching_comments = []
            form = TextForm(request.POST)
            for c in Comments.objects.all():
                if form.data['text_input'] in c.content:
                    matching_comments.append(c)
            if matching_comments:
                array_commentsI = InfoComments(matching_comments, request)
                formC = CercaForm(request.POST)
                formText = TextForm(request.POST)
                return render(request, "app/cercadorComentarisMatch.html",
                              {"comments": array_commentsI, "form": formText, "cercaForm": formC})
            else:
                formCerca = CercaForm(request.POST)
                return render(request, "app/cercadorComentarisNoMatch.html", {"form": form, "cercaForm": formCerca})
    else:
        form = TextComForm()

    return render(request, 'app/layout.html')

def search(request):
    global form
    if request.method == 'POST':
        formName = request.POST['name']
        if formName == "tipusCerca":
            formC = CercaForm(request.POST)
            order_value = formC.data['order']
            if order_value == 'cercapub':
                formText = TextForm(request.POST)
                return render(request, 'app/cercadorPublicacions.html', {"form": formText, "cercaForm": formC})
            if order_value == 'cercacom':
                formText = TextComForm(request.POST)
                return render(request, 'app/cercadorComentaris.html', {"form": formText, "cercaForm": formC})
    else:
        form = CercaForm()

    return render(request, "app/cercador.html", {"cercaForm": form})


# Vista para crear un post
def createPost(request):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            comunities = Community.objects.all()
            return render(request, "app/createPost.html", {
                "options": comunities
            })
        else:
            url = request.POST["url"]
            title = request.POST["title"]
            description = request.POST["description-text"]
            community = request.POST["select-comunity"]
            user = request.user
            c = Community.objects.get(name=community)
            post = Post(url=url, title=title, description=description, community=c, poster=user)
            post.save()
            return HttpResponseRedirect(reverse('index'))


# Vista para renderizar un único post
def post(request, postId):
    postSelected = Post.objects.get(id=postId)
    # de momento devuelvo todos los posts ya que queda lo del login,etc
    if request.method == "GET":
        form = MyForm()
        u = request.user
        p = Post.objects.get(id=postId)
        v = 'caca'
        try:
            b = Votes.objects.get(voter=u, post=p)
            v = b.type
            b = True
        except:
            b = False

        try:
            l = Like.objects.get(user_like=u, post_liked=p)
            liked = True
        except:
            liked = False
        array_comments = []
        com = Comments.objects.filter(post=p, parent=None).order_by('-created_at')
        array_comments = get_info_comments(com,u)
        info_subcomments = get_info_subcomments(postId, u,'New')
        return render(request, "app/post.html", {
            "p": postSelected,
            "comments": array_comments,
            "voted": b,
            "votes": postSelected.positive - postSelected.negative,
            "type": v,
            "liked": liked,
            "infoSubcomments": info_subcomments,
            "form": form
        })
    else:
        u = request.user
        p = Post.objects.get(id=postId)
        v = 'caca'
        try:
            b = Votes.objects.get(voter=u, post=p)
            v = b.type
            b = True
        except:
            b = False

        try:
            l = Like.objects.get(user_like=u, post_liked=p)
            liked = True
        except:
            liked = False
        form = MyForm(request.POST)
        option = form.data['order']
        if option == "New":
            ordComments = Comments.objects.filter(post=postSelected,parent=None).order_by('-created_at')
            array_comments = get_info_comments(ordComments,u)
            info_subcomments = get_info_subcomments(postId,u,option)
            return render(request,"app/post.html", {
                "p": p,
                "comments": array_comments,
                "voted": b,
                "votes": postSelected.positive - postSelected.negative,
                "type": v,
                "liked": liked,
                "infoSubcomments": info_subcomments,
                "form": form
            })
        elif option == 'Old':
            ordComments = Comments.objects.filter(post=postSelected,parent=None).order_by('created_at')
            array_comments = get_info_comments(ordComments,u)
            info_subcomments = get_info_subcomments(postId,u,option)
            return render(request,"app/post.html", {
                "p": p,
                "comments": array_comments,
                "voted": b,
                "votes": postSelected.positive - postSelected.negative,
                "type": v,
                "liked": liked,
                "infoSubcomments": info_subcomments,
                "form": form
            })
        elif option == 'Most comments':
            numcom = OrderedDict()
            ordComments = Comments.objects.filter(post=postSelected,parent=None)
            for c in ordComments:
                numcom[c] = len(c.replies.all())
            numcom = OrderedDict(sorted(numcom.items(), key=lambda item: item[1], reverse=True))
            ordComments = list(numcom.keys())
            array_comments = get_info_comments(ordComments,u)
            info_subcomments = get_info_subcomments(postId,u,option)
            return render(request,"app/post.html", {
                "p": p,
                "comments": array_comments,
                "voted": b,
                "votes": postSelected.positive - postSelected.negative,
                "type": v,
                "liked": liked,
                "infoSubcomments": info_subcomments,
                "form": form
            })
        else: #el millor de tots els temps
            votes = OrderedDict()
            ordComments = Comments.objects.filter(post=postSelected,parent=None)
            for c in ordComments:
                votes[c] = c.resta
            votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
            ordComments = list(votes.keys())
            array_comments = get_info_comments(ordComments,u)
            info_subcomments = get_info_subcomments(postId,u,option)
            return render(request,"app/post.html", {
                "p": p,
                "comments": array_comments,
                "voted": b,
                "votes": postSelected.positive - postSelected.negative,
                "type": v,
                "liked": liked,
                "infoSubcomments": info_subcomments,
                "form": form
            })


def get_info_comments(comments,u):
    array_comments = []
    for c in comments:
        voted = None
        t = None
        lik = None
        try:
            vc = VotesComments.objects.get(voter=u, comment=c)
            voted = True
            t = vc.type
        except:
            voted = False
            t = None
        try:
            lc = LikeComment.objects.get(user_like=u, comment_liked=c)
            lik = True
        except:
            lik = False
        array_comments.append((c, voted, t, lik))
    return array_comments


def get_info_subcomments(postId, u,ordered):
    p = Post.objects.get(id=postId)
    if ordered == "New":
        subcomments = Comments.objects.filter(post=p, parent__isnull=False).order_by('-created_at')
    elif ordered == 'Most comments':
        ordComments = Comments.objects.filter(post=p, parent__isnull=False)
        numcom = OrderedDict()
        for c in ordComments:
            numcom[c] = len(c.replies.all())
        numcom = OrderedDict(sorted(numcom.items(), key=lambda item: item[1], reverse=True))
        subcomments = list(numcom.keys())
    elif ordered == 'Old':
        subcomments = Comments.objects.filter(post=p, parent__isnull=False).order_by('created_at')
    else:
        ordComments = Comments.objects.filter(post=p, parent__isnull=False)
        votes = OrderedDict()
        for c in ordComments:
            votes[c] = c.resta
        votes = OrderedDict(sorted(votes.items(), key=lambda item: item[1], reverse=True))
        subcomments = list(votes.keys())

    info_subcomments = []
    for c in subcomments:
        voted = None
        t = None
        lik = None
        try:
            vc = VotesComments.objects.get(voter=u, comment=c)
            voted = True
            t = vc.type
        except:
            voted = False
            t = None
        try:
            lc = LikeComment.objects.get(user_like=u, comment_liked=c)
            lik = True
        except:
            lik = False
        info_subcomments.append((c.id, voted, t, lik))
    return info_subcomments

def comment(request, postId):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "POST":
            com = request.POST["comentari"]
            user = request.user
            p = Post.objects.get(id=postId)
            p.numComments += 1
            p.save()
            c = Comments(commentor=user, content=com, positive=0, negative=0, post=p,parent=None)
            c.save()
            return HttpResponseRedirect(reverse('post', kwargs={'postId': postId}))


def vote(request, postId, typeV):
    if not request.user.is_authenticated:
        return render(request, template_name="app/login.html")
    updateInfoVotes(request,postId,typeV)
    return HttpResponseRedirect(reverse('post', kwargs={'postId': postId}))


def voteInPosts(request,postId,typeV):
    if not request.user.is_authenticated:
        return render(request, template_name="app/login.html")
    updateInfoVotes(request,postId,typeV)
    return HttpResponseRedirect(reverse('index'))

def voteInProfile(request,postId,typeV,username):
    updateInfoVotes(request,postId,typeV)
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}))

def voteInProfileDesats(request,postId,typeV,username):
    updateInfoVotes(request,postId,typeV)
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Desats')


def updateInfoVotes(request,postId,typeV):

    if request.method == "GET":
        p = Post.objects.get(id=postId)
        u = request.user
        try:
            aux = Votes.objects.get(voter=u, post=p)
        except:
            aux = None
        if typeV == "positive":
            if aux == None:
                v = Votes(voter=u, post=p, type=typeV)
                v.save()
                p.positive = p.positive + 1
                p.save()
            elif aux.type == "positive":
                aux.delete()
                p.positive = p.positive - 1
                p.save()
            elif aux.type == "negative":
                aux.delete()
                v = Votes(voter=u, post=p, type=typeV)
                v.save()
                p.negative = p.negative - 1
                p.positive = p.positive + 1
                p.save()
        else:
            if aux == None:
                v = Votes(voter=u, post=p, type=typeV)
                v.save()
                p.negative = p.negative + 1
                p.save()
            elif aux.type == "negative":
                aux.delete()
                p.negative = p.negative - 1
                p.save()
            elif aux.type == "positive":
                aux.delete()
                v = Votes(voter=u, post=p, type=typeV)
                v.save()
                p.negative = p.negative + 1
                p.positive = p.positive - 1
                p.save()


def like(request, postId):
    updatePostLike(request,postId)
    return HttpResponseRedirect(reverse('post', kwargs={'postId': postId}))

def likeInPosts(request,postId):
    if not request.user.is_authenticated:
        return render(request, template_name="app/login.html")
    updatePostLike(request,postId)
    return HttpResponseRedirect(reverse('index'))

def likeInProfile(request,postId,username):
    if not request.user.is_authenticated:
        return render(request, template_name="app/login.html")
    updatePostLike(request,postId)
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}))

def likeInProfileDesats(request,postId,username):
    if not request.user.is_authenticated:
        return render(request, template_name="app/login.html")
    updatePostLike(request,postId)
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Desats')


def updatePostLike(request,postId):

     if request.method == "GET":
        p = Post.objects.get(id=postId)
        u = request.user
        try:
            l = Like.objects.get(user_like=u, post_liked=p)
        except:
            l = None
        if l == None:
            aux_like = Like(user_like=u, post_liked=p)
            aux_like.save()
        else:
            l.delete()


def likeComment(request, commentId):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            c = Comments.objects.get(id=commentId)
            u = request.user
            try:
                lc = LikeComment.objects.get(user_like=u, comment_liked=c)
            except:
                lc = None
            if lc == None:
                aux_lc = LikeComment(user_like=u, comment_liked=c)
                aux_lc.save()
            else:
                lc.delete()
            return HttpResponseRedirect(reverse('post', kwargs={'postId': c.post.id}))

def likeCommentInProfile(request,commentId,username):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            UpdatelikeComment(commentId,request.user)
            c = Comments.objects.get(id=commentId)
            user = User.objects.get(username=username)
            return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Comentarios')

def likeCommentInProfileDesats(request,commentId,username):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            UpdatelikeComment(commentId,request.user)
            c = Comments.objects.get(id=commentId)
            user = User.objects.get(username=username)
            return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Desats')


def UpdatelikeComment(commentId,u):
    c = Comments.objects.get(id=commentId)
    try:
        lc = LikeComment.objects.get(user_like=u, comment_liked=c)
    except:
        lc = None
    if lc == None:
        aux_lc = LikeComment(user_like=u, comment_liked=c)
        aux_lc.save()
    else:
        lc.delete()


def delete(request, postId):
    if request.method == "GET":
        p = Post.objects.get(id=postId)
        p.delete()
    return HttpResponseRedirect(reverse('index'))


def deleteInProfile(request, postId,username):
    if request.method == "GET":
        p = Post.objects.get(id=postId)
        p.delete()
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}))

def deleteInProfileDesats(request, postId,username):
    if request.method == "GET":
        p = Post.objects.get(id=postId)
        p.delete()
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Desats')


def edit(request, postId):
    p = Post.objects.get(id=postId)
    if request.method == "GET":
        return render(request, "app/edit.html", {
            "p": p,
            "options": Community.objects.all()
        })
    else:
        url = request.POST["url"]
        title = request.POST["title"]
        description = request.POST["description-text"]
        community = request.POST["select-comunity"]
        user = request.user
        c = Community.objects.get(name=community)
        p.url = url
        p.title = title
        p.description = description
        p.community = c
        p.save()
        return HttpResponseRedirect(reverse('post', kwargs={'postId': postId}))


def editComment(request, commentId):
    c = Comments.objects.get(id=commentId)
    if request.method == "GET":
        c.editing = True
        c.save()
    # si es POST(se envio el form, guarda el valor del comentario y devuelve la pagina con el comentario actualizado)
    else:
        content = request.POST["content"]
        c.content = content
        c.editing = False
        c.save()
    return HttpResponseRedirect(reverse('post', kwargs={'postId': c.post.id}))


def cancelEdit(request, commentId):
    if request.method == "GET":
        c = Comments.objects.get(id=commentId)
        c.editing = False
        c.save()
        return HttpResponseRedirect(reverse('post', kwargs={'postId': c.post.id}))


def deleteComment(request, commentId):
    if request.method == "GET":
        c = Comments.objects.get(id=commentId)
        id = c.post.id
        p = Post.objects.get(id=id)
        if (len(c.replies.all()) != 0):
            p.numComments -= len(c.replies.all()) + 1
        else:
            p.numComments -= 1
        p.save()
        c.delete()
        return HttpResponseRedirect(reverse('post', kwargs={'postId': id}))

def deleteCommentInProfile(request, commentId,username):
    if request.method == "GET":
        c = Comments.objects.get(id=commentId)
        id = c.post.id
        p = Post.objects.get(id=id)
        if (len(c.replies.all()) != 0):
            p.numComments -= len(c.replies.all()) + 1
        else:
            p.numComments -= 1
        p.save()
        c.delete()
        user = User.objects.get(username=username)
        return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Comentarios')


def voteComment(request, commentId, typeV):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            updateVoteComment(commentId,typeV,request.user)
            c = Comments.objects.get(id=commentId)
            return HttpResponseRedirect(reverse('post', kwargs={'postId': c.post.id}))

def voteCommentInProfile(request, commentId, typeV, username):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            updateVoteComment(commentId,typeV,request.user)
            user = User.objects.get(username=username)
            return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Comentarios')

def voteCommentInProfileDesats(request, commentId, typeV, username):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            updateVoteComment(commentId,typeV,request.user)
            user = User.objects.get(username=username)
            return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}) + '?button=Desats')

def updateVoteComment(commentId,typeV,u):
    c = Comments.objects.get(id=commentId)
    try:
        aux = VotesComments.objects.get(voter=u, comment=c)
    except:
        aux = None
    if typeV == "positive":
        if aux == None:
            v = VotesComments(voter=u, comment=c, type=typeV)
            v.save()
            c.positive = c.positive + 1
            c.save()
        elif aux.type == "positive":
            aux.delete()
            c.positive = c.positive - 1
            c.save()
        elif aux.type == "negative":
            aux.delete()
            v = VotesComments(voter=u, comment=c, type=typeV)
            v.save()
            c.negative = c.negative - 1
            c.positive = c.positive + 1
            c.save()
    else:
        if aux == None:
            v = VotesComments(voter=u, comment=c, type=typeV)
            v.save()
            c.negative = c.negative + 1
            c.save()
        elif aux.type == "negative":
            aux.delete()
            c.negative = c.negative - 1
            c.save()
        elif aux.type == "positive":
            aux.delete()
            v = VotesComments(voter=u, comment=c, type=typeV)
            v.save()
            c.negative = c.negative + 1
            c.positive = c.positive - 1
            c.save()


def replyComment(request, commentId):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "POST":
            c = Comments.objects.get(id=commentId)
            u = request.user
            contentForm = request.POST["reply_comment"]
            p = Post.objects.get(id=c.post.id)
            p.numComments += 1
            p.save()
            sc = Comments(commentor=u, content=contentForm, parent=c, post=c.post)
            sc.save()
            return HttpResponseRedirect(reverse('post', kwargs={'postId': sc.post.id}))


@login_required
def edit_userProfile(request, username):
    user_profile = User.objects.get(username=username)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('userProfile', username=request.user.username)

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'app/editUserProfile.html', {
        'profile_form': form,
    })

def createCommunity(request):
    user = request.user
    if request.method == "GET":
        return render(request, template_name = "app/createCommunity.html")
    elif user.is_authenticated:
        id = request.POST["id"]
        name = request.POST["name"]
        banner = request.POST["banner"]
        avatar = request.POST["avatar"]
        community = Community(id = id, name = name, banner = banner, avatar = avatar)
        community.save()
        v = []
        sub = Subscription.objects.filter(user_sub=user)
        for s in sub:
            v.append((s.community_sub, True))
        return render(request, template_name="app/listCommunity.html", context={
            "communities": v
        })
    else:
        return render(request, template_name="app/login.html")

def listCommunity(request):
    user = request.user
    if user.is_authenticated:
        button = request.GET.get('button')
        user = request.user
        sub = Subscription.objects.filter(user_sub=user)
        if button == 'Subscrit':
            v = []
            for s in sub:
                v.append((s.community_sub, True))
            return render(request, template_name="app/listCommunity.html", context={
                "communities": v
            })
        else:
            com = Community.objects.all()
            v = []
            for c in com:
                try:
                    sub = Subscription.objects.get(user_sub=user, community_sub=c)
                except:
                    sub = None
                if sub == None:
                    v.append((c, False))
                else:
                    v.append((c, True))
            return render(request, template_name="app/listCommunity.html", context={
                "communities": v})
    else:
        com = Community.objects.all()
        v = []
        for c in com:
            v.append((c, False))
        return render(request, template_name="app/listCommunity.html", context={
            "communities": v
        })

def subscribeCommunity(request, community_name):
    if request.method == "GET":
        user_sub = request.user
        if user_sub.is_authenticated:
            community_sub = Community.objects.get(name=community_name)
            sub = None
            try:
                sub = Subscription.objects.get(user_sub=user_sub, community_sub=community_sub)
            except:
                sub = None
            if sub is None:
                sub = Subscription(user_sub=user_sub, community_sub=community_sub)
                sub.save()
            else:
                sub.delete()

            return HttpResponseRedirect(reverse('listCommunity'))
        else:
            return render(request, template_name="app/login.html")

def viewCommunity(request, community_name):
    if request.method == "GET":
        button = request.GET.get('button')
        user = request.user
        community = Community.objects.get(name=community_name)
        posts = Post.objects.filter(community=community)
        info_posts = infopost(posts, request)
        if button == 'Publicaciones':
            bool = False
            return render(request, template_name="app/viewCommunity.html", context= {
                'posts': info_posts,
                'comments': [],
                'community': community,
                'bool': bool
            })
        else:
            v = []
            bool = True
            for p in posts:
                comments = Comments.objects.filter(post=p)
                for co in comments:
                    v.append(co)
            info_comments = InfoComments(v, request)
            return render(request, template_name="app/viewCommunity.html", context= {
                'posts': [],
                'comments': info_comments,
                'community': community,
                'bool': bool
            })
    else:
        return HttpResponseRedirect(reverse('listCommunity'))


def voteInCommunity(request, postId, typeV, community_name):
    if not request.user.is_authenticated:
        return render(request, template_name="app/login.html")
    updateInfoVotes(request, postId, typeV)
    return HttpResponseRedirect(reverse('viewCommunity', kwargs={'community_name': community_name})+'?button=Publicaciones')

def likeInCommunity(request,postId, community_name):
    if not request.user.is_authenticated:
        return render(request, template_name="app/login.html")
    updatePostLike(request,postId)
    return HttpResponseRedirect(reverse('viewCommunity', kwargs={'community_name': community_name})+'?button=Publicaciones')

def voteCommentInCommunity(request, commentId, typeV, community_name):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            c = Comments.objects.get(id=commentId)
            u = request.user
            try:
                aux = VotesComments.objects.get(voter=u, comment=c)
            except:
                aux = None
            if typeV == "positive":
                if aux == None:
                    v = VotesComments(voter=u, comment=c, type=typeV)
                    v.save()
                    c.positive = c.positive + 1
                    c.save()
                elif aux.type == "positive":
                    aux.delete()
                    c.positive = c.positive - 1
                    c.save()
                elif aux.type == "negative":
                    aux.delete()
                    v = VotesComments(voter=u, comment=c, type=typeV)
                    v.save()
                    c.negative = c.negative - 1
                    c.positive = c.positive + 1
                    c.save()
            else:
                if aux == None:
                    v = VotesComments(voter=u, comment=c, type=typeV)
                    v.save()
                    c.negative = c.negative + 1
                    c.save()
                elif aux.type == "negative":
                    aux.delete()
                    c.negative = c.negative - 1
                    c.save()
                elif aux.type == "positive":
                    aux.delete()
                    v = VotesComments(voter=u, comment=c, type=typeV)
                    v.save()
                    c.negative = c.negative + 1
                    c.positive = c.positive - 1
                    c.save()
            return HttpResponseRedirect(reverse('viewCommunity', kwargs={'community_name': community_name})+'?button=?button=Comentarios')

def likeCommentInCommunity(request, commentId, community_name):
    if request.user.is_anonymous:
        return render(request, "app/login.html")
    else:
        if request.method == "GET":
            c = Comments.objects.get(id=commentId)
            u = request.user
            try:
                lc = LikeComment.objects.get(user_like=u, comment_liked=c)
            except:
                lc = None
            if lc == None:
                aux_lc = LikeComment(user_like=u, comment_liked=c)
                aux_lc.save()
            else:
                lc.delete()
            return HttpResponseRedirect(reverse('viewCommunity', kwargs={'community_name': community_name})+'?button=?button=Comentarios')

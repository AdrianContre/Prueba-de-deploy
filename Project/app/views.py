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

def index(request):
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
        infoPosts.append((p,b,v,liked))
        

    return render(request, "app/posts.html", {"posts": infoPosts,"form": form})

def view_userProfile(request, username):
    try:
        user_profile = User.objects.get(username=username)
        user_posts = Post.objects.filter(poster=user_profile).order_by('-created_at')
        user_comments = Comment.objects.filter(user_profile=user_profile)
        button = request.GET.get('button', 'Publicaciones')  # Por defecto a 'Publicaciones'
        liked_posts = Like.objects.filter(user_like=user_profile)
        liked_comments = LikeComment.objects.filter(user_like=user_profile)

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

        liked_posts_info = [(lp.post_liked, None, None, True) for lp in liked_posts]
        liked_comments_info = [(lc.comment_liked, None, None, True) for lc in liked_comments]

    except User.DoesNotExist:
        raise Http404("El usuario no existe")

    return render(request, 'app/userProfile.html', {
        'user_profile': user_profile,
        'user_posts': infoPosts,
        'user_comments': array_comments,
        'button': button,
        'like_posts': liked_posts_info,
        'like_comments': liked_comments_info,
    })
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
                u = request.user
                array_comments = []
                for c in matching_comments:
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
                formC = CercaForm(request.POST)
                formText = TextForm(request.POST)
                return render(request, "app/cercadorComentarisMatch.html",
                              {"comments": array_comments, "form": formText, "cercaForm": formC})
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

def boto_rar(request):
    user = request.user
    form = MyForm(request.POST)
    ordPost = Post.objects.all().order_by('-created_at')
    button = request.GET.get('button')
    if user.is_authenticated:
        sub = Subscription.objects.filter(user_sub=user)
        if button == 'Subscrit':
            v = []
            for s in sub:
                v.append(Post.objects.filter(community=s.community_sub))
            l = np.concatenate(v)
            return render(request, "app/posts.html", {"posts": l, "form": form})
        else:
            return render(request, "app/posts.html", {"posts": ordPost, "form": form})
    else:
        return render(request, template_name="app/login.html")


# Vista para crear un post
def createPost(request):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "GET":
            comunities = Community.objects.all()
            print(comunities)
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
        com = Comments.objects.filter(post=p, parent=None)
        for c in com:
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

        info_subcomments = get_info_subcomments(postId, u)
        return render(request, "app/post.html", {
            "p": postSelected,
            "comments": array_comments,
            "voted": b,
            "votes": postSelected.positive - postSelected.negative,
            "type": v,
            "liked": liked,
            "infoSubcomments": info_subcomments
        })


def get_info_subcomments(postId, u):
    p = Post.objects.get(id=postId)
    subcomments = Comments.objects.filter(post=p, parent__isnull=False)
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
    updateInfoVotes(request,postId,typeV)
    return HttpResponseRedirect(reverse('post', kwargs={'postId': postId}))


def voteInPosts(request,postId,typeV):
    updateInfoVotes(request,postId,typeV)
    return HttpResponseRedirect(reverse('index'))

def voteInProfile(request,postId,typeV,username):
    updateInfoVotes(request,postId,typeV)
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}))


def updateInfoVotes(request,postId,typeV):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
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
    updatePostLike(request,postId)
    return HttpResponseRedirect(reverse('index'))

def likeInProfile(request,postId,username):
    updatePostLike(request,postId)
    user = User.objects.get(username=username)
    return HttpResponseRedirect(reverse('userProfile', kwargs={'username': user.username}))


def updatePostLike(request,postId):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
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


def delete(request, postId):
    if request.method == "GET":
        p = Post.objects.get(id=postId)
        p.delete()
    return HttpResponseRedirect(reverse('index'))


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
        print(community)
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
        c.delete()
        return HttpResponseRedirect(reverse('post', kwargs={'postId': id}))


def voteComment(request, commentId, typeV):
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
            return HttpResponseRedirect(reverse('post', kwargs={'postId': c.post.id}))


def replyComment(request, commentId):
    if request.user.is_anonymous:
        return render(request,"app/login.html")
    else:
        if request.method == "POST":
            print(commentId)
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
    if request.method == "GET":
        return render(request, template_name = "app/createCommunity.html")
    else:
        id = request.POST["id"]
        name = request.POST["name"]
        banner = request.POST["banner"]
        avatar = request.POST["avatar"]
        community = Community(id = id, name = name, banner = banner, avatar = avatar)
        community.save()
        return HttpResponseRedirect(reverse('index'))

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


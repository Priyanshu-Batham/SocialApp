from django.shortcuts import render, redirect, HttpResponse
from .models import Post, Follow, Comment, Like
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import PostForm
from django.urls import reverse


# Create your views here.
def homepage(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        likes = Like.objects.filter(likedPost=post)
        post.likes = len(likes)
    context={
        'posts': posts
    }
    return render(request, 'homepage.html', context)

def profile(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.filter(user=user).order_by('-created_at')
        for post in posts:
            likes = Like.objects.filter(likedPost=post)
            post.likes = len(likes)
        followers = Follow.objects.filter(following=user)
        following = Follow.objects.filter(follower=user)

        form = PostForm()
        
        context={
            'user': user,
            'posts': posts,
            'form': form,
            'followers': followers,
            'following': following,
        }
        return render(request, 'profile.html', context)
    
    return redirect('/auth/login')

def create_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        print(request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            #doing this bcoz i want the post instance before saving in db
            post = form.save(commit=False)
            #now i'll add user in my post instance
            post.user = request.user
            #and finally save the post instance in db
            post.save()
            return redirect('profile')
    
    return redirect('profile')

def delete_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.filter(id=id).first()
        
        if request.user == post.user:
            post.delete()
            return redirect('profile')
    
    return redirect('profile')

def showuser(request, id):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    user = User.objects.filter(id=id).first()
    if not user:
        return HttpResponse("user not found") 
    if user == request.user:
        return redirect('profile')
    posts = Post.objects.filter(user=user).order_by('-created_at')
    for post in posts:
        likes = Like.objects.filter(likedPost=post)
        post.likes = len(likes)
    followers = Follow.objects.filter(following=user)
    following = Follow.objects.filter(follower=user)
    doIFollow = Follow.objects.filter(follower=request.user, following=user).exists()

    context={
            'user': user,
            'posts': posts,
            'followers': followers,
            'following': following,
            'doIFollow': doIFollow,
        }
    return render(request, 'showuser.html', context)

def follow(request, id):
    if request.user.is_authenticated:
        userToFollow = User.objects.filter(id=id).first()
        if userToFollow:
            created = Follow.objects.create(follower=request.user, following=userToFollow)
            if created:
                # Generate the absolute URL using reverse
                url = reverse('showuser', kwargs={'id': id})
                return redirect(url)
           
    
    return redirect('profile')

def unfollow(request, id):
    if request.user.is_authenticated:
        userToUnFollow = User.objects.filter(id=id).first()
        if userToUnFollow:
            Follow.objects.filter(follower=request.user, following=userToUnFollow).delete()
            
            # Generate the absolute URL using reverse
            url = reverse('showuser', kwargs={'id': id})
            return redirect(url)
           
    
    return redirect('profile')

def post(request, id):
    post = Post.objects.filter(id=id).first()
    comments = Comment.objects.filter(post=post)
    likes = Like.objects.filter(likedPost=post)
    doILike = False
    try:
        doILike = likes.filter(likedBy=request.user)
    except(Exception):
        pass
    
    context={
        'post':post,
        'comments': comments,
        'likes': likes,
        'doILike': doILike,
    }
    
    return render(request, 'post.html', context)

def add_comment(request, postid):
    comm = request.POST.get('comment')
    post = Post.objects.get(id=postid)
    if request.user.is_authenticated:
        comment = Comment.objects.create(user=request.user, comment=comm, post=post)
        comment.save()
        url = reverse('post', kwargs={'id': postid})
        return redirect(url)


def like_post(request, postid):
    if not request.user.is_authenticated:
        return redirect("/auth/login")
    
    post = Post.objects.get(id=postid)
    try:
        liked = Like.objects.create(likedBy=request.user, likedPost=post)
        liked.save()
    except(Exception):
        #if user has already liked this post but illegaly hitting this url tryna hack the sys lmao
        pass
    finally:
        url = reverse('post', kwargs={'id': postid})
        return redirect(url)
    
def unlike_post(request, postid):
    if not request.user.is_authenticated:
        return redirect("/auth/login")
    
    post = Post.objects.get(id=postid)
    try:
        liked = Like.objects.get(likedBy=request.user, likedPost=post)
        liked.delete()
    except(Exception):
        pass
    finally:
        url = reverse('post', kwargs={'id': postid})
        return redirect(url)



#AUTHENTICATIONS FUNCTIONS
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  # Redirect to the homepage after successful login      
        
            #here all the else parts are to be written for better UX    
        
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')
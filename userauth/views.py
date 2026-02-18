from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import LikePost, Profile,Post,Followers
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


def landing(request):
    return render(request, 'landing.html')


def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        # check if user already exists
        if User.objects.filter(username=fnm).exists():
            invalid = "User Already Exists"
            return render(request, 'signup.html', {'invalid': invalid})
        # create user
        my_user = User.objects.create_user(
            username=fnm,
            email=emailid,
            password=pwd
        )


        return redirect('login')


    # ✅ THIS WAS MISSING (GET request)
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=fnm, password=pwd)

        if user is not None:
            auth_login(request, user)
            return redirect('home')   # 🔥 go to home page after login
        else:
            invalid = "Invalid Credentials"
            return render(request, 'login.html', {'invalid': invalid})

    return render(request, 'login.html')


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required(login_url='/login')
def upload(request):

    if request.method == 'POST':

        if request.FILES.get('image_upload'):
            user = request.user.username
            image = request.FILES.get('image_upload')
            caption = request.POST.get('caption')

            Post.objects.create(
                user=user,
                image=image,
                caption=caption
            )

            return redirect(f'/profile/{user}')

    return redirect('/')



@login_required(login_url='/login')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = LikePost.objects.filter(post_id=id, username=username).first()

        if like_filter is None:
            LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes += 1
        else:
            like_filter.delete()
            post.no_of_likes -= 1

        post.save()

        return redirect(f'/home/#post{id}')

@login_required(login_url='/login')
def home(request):
    following_users = Followers.objects.filter(followers=request.user.username).values_list('user',flat=True)
    posts = Post.objects.filter(Q(user=request.user.username)|Q (user__in=following_users)).order_by('-created_at')
    profile = Profile.objects.get(user=request.user)
    username = request.user.username

    for post in posts:
        liked = LikePost.objects.filter(post_id=post.id, username=username).first()
        if liked:
            post.liked = True
        else:
            post.liked = False

    return render(request, "main.html", {
        "posts": posts,
        "profile": profile 
        })

@login_required(login_url='/login')
def explore(request):
    posts = Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)
    context={
        'posts':posts,
         'profile':profile
    }
    return render(request,'explore.html',context)


@login_required(login_url='/login')
def profile(request, id_user):

    user_object = User.objects.get(username=id_user)

    # safe profile get
    user_profile, created = Profile.objects.get_or_create(user=user_object) 

    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
    
       

    user_post_length = user_posts.count()

    follower =request.user.username
    user =id_user
    if Followers.objects.filter(followers=follower, user=user).first():
    
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = Followers.objects.filter(user=id_user).count()
    user_following = Followers.objects.filter(followers=id_user).count()
        

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': Profile.objects.get(user=request.user),  # sidebar login user
        'follow_unfollow':follow_unfollow,
        'user_following':user_following,
        'user_followers':user_followers,
                                }

    if request.user.username ==id_user:
        if request.method == 'POST':
            if request.FILES.get('image')==None:
                image=user_profile.profileimg
                bio=request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg=image
                user_profile.bio=bio
                user_profile.location = location
                user_profile.save()
            if request.FILES.get('image') !=None: 
                image=request.FILES.get('image')
                bio=request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg=image
                user_profile.bio=bio
                user_profile.location=location
                user_profile.save() 
            return redirect('/profile/'+id_user)   
        else:
            return render(request,'profile.html',context)   
    return render(request, 'profile.html', context)

@login_required(login_url='/login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user=request.POST['user']

      
        if Followers.objects.filter(followers=follower, user=user).first():
         delete_follower = Followers.objects.get(followers=follower, user=user)
         delete_follower.delete()
         return redirect('/profile/'+user)
        else:
         new_follower = Followers.objects.create(followers=follower,user=user)
         new_follower.save()
         return redirect('/profile/'+user)
    else:
     return redirect('/')    

@login_required(login_url='/login')
def delete(request, id):
    print("DELETE ID:", id)

    post = get_object_or_404(Post, id=id)

    # 🔥 FIX HERE
    if post.user == request.user.username:
        post.delete()
        print("DELETED SUCCESS")

    return redirect('/profile/' + request.user.username)


@login_required(login_url='/login')
def search_results(request):
    query = request.GET.get('q')
    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)
    context = {
        'query':query,
        'users':users,
        'posts':posts
    }
    return render(request, 'search_user.html', context)


@login_required(login_url='/login')
def logout_view(request):
    auth_logout(request)
    return redirect('/login')

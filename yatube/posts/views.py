from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.decorators.cache import cache_page
import markdown

from .models import Group, Post, Follow, Comment
from .my_paginator import paginate_queryset
from .forms import CommentForm, PostForm

User = get_user_model()


@cache_page(20, key_prefix='index_page')
def index(request):
    group = Group.objects.all()
    post_list = Post.objects.select_related('author', 'group')
    page_obj = paginate_queryset(post_list, request)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    # post_list = group.posts.select_related('author')
    post_list = Post.objects.filter(group=group)
    page_obj = paginate_queryset(post_list, request)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    # post_list = author.posts.all()
    post_list = Post.objects.filter(author=author)
    page_obj = paginate_queryset(post_list, request)
    following = (
        request.user.is_authenticated and Follow.objects.filter(
            user=request.user.pk, author=author).exists())
    context = {
        'author': author,
        'page_obj': page_obj,
        'number_post_list': post_list.count,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    num_posts = Post.objects.filter(
        author__username=post.author).count
    form = CommentForm()
    # comments = post.comments.all()
    comments = Comment.objects.filter(post=post)
    comments_count = comments.count()
    interesting_posts = Post.objects.filter(group=post.group)
    context = {
        'post': post,
        'num_posts': num_posts,
        'form': form,
        'comments': comments,
        'comments_count': comments_count,
        'interesting_posts': interesting_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required(login_url='/auth/login/')
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.text = markdown.markdown(post.text,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        form.save()
        return HttpResponseRedirect(f'/profile/{request.user.username}/')
    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.text = markdown.markdown(post.text,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    if post.author.id != request.user.id:
        return HttpResponseRedirect(reverse(
            'posts:post_detail', args=[post_id]))
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None, instance=post)
        if form.is_valid():
            f = form.save(commit=False)
            f.author_id = request.user.id
            form.save()
            return redirect(f'/posts/{post.id}/', {'form': form})

    form = PostForm(
        instance=post,
        files=request.FILES or None
    )
    context = {
        'post_id': post_id,
        'is_edit': True,
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required(login_url='/auth/login/')
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.text = markdown.markdown(comment.text,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required(login_url='/auth/login/')
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginate_queryset(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required(login_url='/auth/login/')
def profile_follow(request, username):
    # Подписаться на автора
    follower = User.objects.get(username=username)
    if not request.user == follower:
        Follow.objects.get_or_create(user=request.user, author=follower)
    return redirect('posts:follow_index')


@login_required(login_url='/auth/login/')
def profile_unfollow(request, username):
    # Дизлайк, отписка
    follower = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, author=follower).delete()
    return redirect('posts:follow_index')

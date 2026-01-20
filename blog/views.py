from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """Display all published blog posts"""
    posts = Post.objects.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, slug):
    """Display a single blog post"""
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, 'blog/post_detail.html', {'post': post})

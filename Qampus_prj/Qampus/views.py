from django.shortcuts import render, redirect
from .models import Category, Post
from django.shortcuts import get_object_or_404

def main(request, slug=None):
    categories = Category.objects.all()

    posts = Post.objects.all().order_by('-created_at')

    current_category = None
    if slug:
        current_category = get_object_or_404(Category, slug=slug)
        posts = posts.filter(category=current_category)

    context = {
        "categories" : categories, 
        "posts" : posts, 
        "current_category" : current_category, 
    }
    return render(request, 'Qampus/main.html', {'posts':posts, 'context':context})

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        posts = Post.objects.create(
            title = title,
            content = content,
            author = request.user,
            category = category,
        )
        return redirect('Qampus:main')
    categories = Category.objects.all()
    return render(request, 'Qampus/create.html', {'categories' : categories})

def detail(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        content = request.POST.get('content')
    return render(request, 'Qampus/detail.html', {'post':post, 'comments': comments})

def update(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('Qampus:detail', id)
    return render(request, 'Qampus/update.html', {'post':post})

def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('Qampus:main')

def category(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')

    return render(request, 'Qampus/category.html', {'category':category, 'posts':posts})

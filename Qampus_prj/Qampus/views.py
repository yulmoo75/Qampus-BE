from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404

def main(request):
    category_slug = request.POST.get('category_slug', '')
    sort = request.POST.get('sort', 'latest')

    if category_slug:
        posts = Post.objects.filter(category__slug=category_slug).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    if sort == 'popular':
        posts = posts.order_by('-likes')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'Qampus/main.html', {'posts': posts, 'selected_slug': category_slug, 'sort':sort})
    
def create(request, slug=None):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')

        Post.objects.create(
            title = title,
            content = content,
            category_id = category_id,
        )
        return redirect('Qampus:main')
    categories = Category.objects.all()
    return render(request, 'Qampus/create.html', {'categories' : categories})

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')
    comment_count = post.comments.count()
    like_count = post.likes.count()
    reply_count = Reply.objects.filter(comment__post=post).count()
    total_comment_count = comment_count + reply_count

    if request.method == 'POST':
        content = request.POST.get('content')
    return render(request, 'Qampus/detail.html', 
                {'post':post,
                'comments': comments,
                'like_count': post.like_count,
                'scrap_count': post.scrap_count,
                'comment_count': total_comment_count,
                'content':content})

def update(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('Qampus:detail', id)
    categories = Category.objects.all()
    return render(request, 'Qampus/update.html', {'post':post, 'categories':categories})

def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('Qampus:main')

def category(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category).order_by('-created_at')

    return render(request, 'Qampus/category.html', {'category':category, 'posts':posts})


#답변 CRUD
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Comment.objects.create(
                post=post,
                content=content
            )

    return redirect("Qampus:detail", post_id)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id

    comment.delete()

    return redirect("Qampus:detail", post_id)


def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            comment.content = content
            comment.save()

    return redirect("Qampus:detail", post_id)


#대댓글 CRUD
def create_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Reply.objects.create(
                comment=comment,
                content=content
            )

    return redirect("Qampus:detail", comment.post.id)


def update_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            reply.content = content
            reply.save()

    return redirect("Qampus:detail", reply.comment.post.id)


def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    post_id = reply.comment.post.id

    reply.delete()

    return redirect("Qampus:detail", post_id)

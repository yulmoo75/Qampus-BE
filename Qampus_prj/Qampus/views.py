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
        posts = posts.order_by('-like_count')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'Qampus/main.html', {'posts': posts, 'selected_slug': category_slug, 'sort':sort})
    
def create(request, slug=None):
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_ids = request.POST.getlist('category')
        category_list = [get_object_or_404(Category, id=category_id) for category_id in category_ids]

        post = Post.objects.create(
            title = title,
            content = content,
        )

        for category in category_list:
            post.category.add(category)
        return redirect('Qampus:main')
    return render(request, 'Qampus/create.html', {'categories' : categories})

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')
    comment_count = post.comments.count()
    reply_count = Reply.objects.filter(comment__post=post).count()
    total_comment_count = comment_count + reply_count
    like_count = post.like_count
    scrap_count = post.scrap_count

    content = ''
    if request.method == 'POST':
        content = request.POST.get('content')
    return render(request, 'Qampus/detail.html', 
                {'post':post,
                'comments': comments,
                'like_count': like_count,
                'scrap_count': scrap_count,
                'comment_count': total_comment_count,
                })

def update(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        
        category_ids = request.POST.getlist('category')

        if category_ids:
            updated_categories = Category.objects.filter(id__in=category_ids)
            post.category.set(updated_categories)
        else:
            post.category.clear()
            
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


#게시글 스크랩
def scrap_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    scrapped_posts = request.session.get('scrapped_posts', [])

    if post_id in scrapped_posts:
        if post.scrap_count > 0:
            post.scrap_count -= 1
        scrapped_posts.remove(post_id)
    else:
        post.scrap_count += 1
        scrapped_posts.append(post_id)

    post.save()
    request.session['scrapped_posts'] = scrapped_posts

    return redirect('Qampus:detail', post.id)

#게시글 좋아요
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    liked_posts = request.session.get('liked_posts', [])

    if post_id in liked_posts:
        if post.like_count > 0:
            post.like_count -= 1
        liked_posts.remove(post_id)
    else:
        post.like_count += 1
        liked_posts.append(post_id)

    post.save()
    request.session['liked_posts'] = liked_posts

    return redirect('Qampus:detail', post.id)


#댓글/대댓글 좋아요
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    liked_comments = request.session.get('liked_comments', [])

    if comment_id in liked_comments:
        if comment.like_count > 0:
            comment.like_count -= 1
        liked_comments.remove(comment_id)
    else:
        comment.like_count += 1
        liked_comments.append(comment_id)

    comment.save()
    request.session['liked_comments'] = liked_comments

    return redirect('Qampus:detail', comment.post.id)


def like_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    liked_replies = request.session.get('liked_replies', [])

    if reply_id in liked_replies:
        if reply.like_count > 0:
            reply.like_count -= 1
        liked_replies.remove(reply_id)
    else:
        reply.like_count += 1
        liked_replies.append(reply_id)

    reply.save()
    request.session['liked_replies'] = liked_replies
    return redirect('Qampus:detail', reply.comment.post.id)

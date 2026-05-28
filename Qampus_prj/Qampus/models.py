from django.db import models

class Category(models.Model):
    name = models.CharField(max_length= 50, unique= True)
    slug = models.SlugField(max_length= 100, unique= True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length= 50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    category = models.ManyToManyField(Category, related_name="posts")    
    like_count = models.PositiveIntegerField(default=0)
    scrap_count = models.PositiveIntegerField(default=0)
    likes = models.PositiveBigIntegerField(default=0)
    scraps = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'[{self.id}] self.title'
    
class PostCategory(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="post_categories")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="post_categories")

    
class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'[{self.id}] {self.content}'
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.id}] {self.content[:20]}'
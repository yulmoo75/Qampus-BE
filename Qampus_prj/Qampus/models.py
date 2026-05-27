from django.db import models
#from users.models import User

class Category(models.Model):
    name = models.CharField(max_length= 50, unique= True)
    slug = models.SlugField(max_length= 100, unique= True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length= 50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add= True)
    likes = models.PositiveBigIntegerField(default=0)
    scraps = models.PositiveBigIntegerField(default=0)
    #charfield로 해서 defaul=응답자, 글 작성시에 이름 받기..? author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f'[{self.id}] {self.title}'
    
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

    def __str__(self):
        return f'[{self.id}] {self.content}'
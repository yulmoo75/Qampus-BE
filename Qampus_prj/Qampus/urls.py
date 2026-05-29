from django.urls import path
from .views import *

app_name = 'Qampus'

urlpatterns = [
    path('', main, name='main'), 
    path('create/', create, name='create'),
    path('detail/<int:id>', detail, name='detail'), 
    path('update/<int:id>', update, name='update'), 
    path('delete/<int:id>', delete, name='delete'), 
    path('category/<slug:slug>/', main, name='category'),
    path("posts/<int:post_id>/comments/create/", create_comment, name="create_comment"),
    path("comments/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path("comments/<int:comment_id>/update/", update_comment, name="update_comment"),
    path("comments/<int:comment_id>/replies/create/", create_reply, name="create_reply"),
    path("replies/<int:reply_id>/update/", update_reply, name="update_reply"),
    path("replies/<int:reply_id>/delete/", delete_reply, name="delete_reply"),
    path("posts/<int:post_id>/scrap/", scrap_post, name="scrap_post"),
    path("posts/<int:post_id>/like/", like_post, name="like_post"),
]
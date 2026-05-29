from django.urls import path
from .views import *

app_name = 'Qampus'

urlpatterns = [
    path('', main, name='main'), 
    path('create/', create, name='create'),
    path('detail/<int:id>/', detail, name='detail'), 
    path('update/<int:id>/', update, name='update'), 
    path('delete/<int:id>/', delete, name='delete'), 
    path('category/<slug:slug>/', category, name='category'),
    path("posts/<int:post_id>/comments/create/", create_comment, name="create_comment"),
    path("comments/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path("comments/<int:comment_id>/update/", update_comment, name="update_comment"),
    path("comments/<int:comment_id>/replies/create/", create_reply, name="create_reply"),
    path("replies/<int:reply_id>/update/", update_reply, name="update_reply"),
    path("replies/<int:reply_id>/delete/", delete_reply, name="delete_reply"),
    path('api/posts/', api_post_list, name='api_post_list'), 
    path('api/posts/<int:id>/', api_post_detail, name='api_post_detail'),
    path('api/posts/create/', api_post_create, name='api_post_create'),
    path('api/posts/<int:id>/update/', api_post_update, name='api_post_update'),
]
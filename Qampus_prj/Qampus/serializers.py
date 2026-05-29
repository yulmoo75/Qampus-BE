from rest_framework import serializers
from .models import Post, Category, Comment

class CommentSerializer(serializers.ModelSerializer):
    ..

class PostListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = 'name',
        source = 'category'
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'created_at', 'like_count', 'scrap_count', 
        ]

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("제목은 공백으로 작성할 수 없습니다.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("내용을 입력해주세요.")
        return value
    
class PostDetailSerializer(serializers.ModelSerializer):
    category_names = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name', source='category'
    )
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category_names', 
            'created_at', 'comment_count', 'comments'
        ]

    def get_comment_count(self, obj):
        return obj.comments.count()
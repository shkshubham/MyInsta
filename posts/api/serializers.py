from rest_framework.serializers import ModelSerializer
from posts.models import Post, Like
from accounts.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',            
            ]

class LikeSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Like
        fields = [
            'user',
            'post',
            ]

class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'photo',
            'caption',
            ]

class PostListSerializer(ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Post
        fields = [
            'author',
            'photo',
            'caption',
            ]

class PostDetailSerializer(ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Post
        fields = [
            'author',
            'photo',
            'caption',
            ]
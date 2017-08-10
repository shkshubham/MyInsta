from rest_framework.serializers import ModelSerializer
from posts.models import Post, Like
from accounts.models import User


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'caption',
            'photo'
            ]


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'gender',
            'avatar',            
            ]


class UserDetailSerializer(ModelSerializer):
        class Meta:
            model = User    
            fields = [
            'username',
            'name',
            'gender',
            'avatar',
            'contact',
            'date_of_birth',
            'quote', 
            ]

class UserUpdateSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'name',
            'gender',
            'avatar',
            'contact',
            'date_of_birth',
            'quote',
            ]
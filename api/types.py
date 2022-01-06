from graphene_django import DjangoObjectType

from db.models import Category, Keyword, Post
from django.contrib.auth import get_user_model


class CategoryType(DjangoObjectType):
    # Meta class is required
    class Meta:
        # model is required
        model = Category
        fields = '__all__'


class KeywordType(DjangoObjectType):
    class Meta:
        model = Keyword
        fields = '__all__'


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'posts',)

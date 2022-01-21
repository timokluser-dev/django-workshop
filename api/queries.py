import graphene
from graphql_jwt.decorators import login_required

from db.models import Category, Keyword, Post
from django.contrib.auth import get_user_model
from api.types import CategoryType, KeywordType, PostType, UserType


class HelloQuery(graphene.ObjectType):
    hello = graphene.String(default_value='Hi!', description='Dummy endpoint to say hi')


class CategoryQuery(graphene.ObjectType):
    # <Model>_list
    category_list = graphene.List(CategoryType, description='Get all categories')
    # <Model>_detail - get by id
    category_detail = graphene.Field(CategoryType, id=graphene.ID(required=True), description='Get category by Id')

    # prefix: resolve_<field>
    @login_required
    def resolve_category_list(self, info, **kwargs):
        # models.Model.objects.all()
        return Category.objects.all()

    # kwargs = keyword arguments -> object
    #   my_func(hello="world")
    # args = list of arguments -> array
    #   my_func("hello", "world")
    @login_required
    def resolve_category_detail(self, info, id, **kwargs):
        return Category.objects.get(id=id)  # Category.objects.get(id=kwargs.get('id'))


class KeywordQuery(graphene.ObjectType):
    keyword_list = graphene.List(KeywordType, description='Get all keywords')
    keyword_detail = graphene.Field(KeywordType, id=graphene.ID(required=True), description='Get keyword by Id')

    @login_required
    def resolve_keyword_list(self, info, **kwargs):
        return Keyword.objects.all()

    @login_required
    def resolve_keyword_detail(self, info, id, **kwargs):
        return Keyword.objects.get(id=id)


class PostQuery(graphene.ObjectType):
    post_list = graphene.List(PostType, category_id=graphene.ID(required=False), keyword_id=graphene.ID(required=False),
                              description='Get posts, optionally by categoryId or keywordId')
    post_detail = graphene.Field(PostType, id=graphene.ID(required=True), description='Get post by Id')

    def resolve_post_list(self, info, category_id=None, keyword_id=None, **kwargs):
        filters = {}
        if category_id:
            filters['category_id'] = category_id
        if keyword_id:
            filters['keywords'] = keyword_id

        # Performance optimize:
        # select_related("model") = inner join
        # prefetch_related("model") = join on cross table
        return Post.objects.select_related("category").prefetch_related("keywords").filter(**filters)

    def resolve_post_detail(self, info, id, **kwargs):
        return Post.objects.select_related("category").prefetch_related("keywords").get(id=id)


class UserQuery(graphene.ObjectType):
    # scalars: parameters for queries
    # https://docs.graphene-python.org/en/latest/types/scalars/
    user_detail = graphene.Field(UserType, username=graphene.String(required=True), description='Get user by username')
    me = graphene.Field(UserType, description='Get logged in user profile')

    @login_required
    def resolve_user_detail(self, info, username, **kwargs):
        return get_user_model().objects.prefetch_related("posts").get(username=username)

    @login_required
    def resolve_me(self, info, **kwargs):
        # current user: info.context.user
        return get_user_model().objects.prefetch_related("posts").get(username=info.context.user.username)

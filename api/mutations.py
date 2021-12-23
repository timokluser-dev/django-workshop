import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from api.types import PostType
from api.forms import PostForm


# Django Form
# see: https://medium.com/@aacha002/graphql-django-djangomodelformmutation-walkthrough-b0d62364b1ee
class PostMutation(DjangoModelFormMutation):
    post = graphene.Field(PostType)

    class Meta:
        form_class = PostForm


class PostMutation(graphene.ObjectType):
    create_post = PostMutation.Field()
    update_post = PostMutation.Field()

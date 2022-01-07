import graphene
import graphql_jwt
from graphql_jwt.decorators import permission_required, login_required
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_file_upload.scalars import Upload
from PIL import Image

from api.inputs import PostInput
from api.types import PostType
from db.models import Post


# Django Form
# see: https://medium.com/@aacha002/graphql-django-djangomodelformmutation-walkthrough-b0d62364b1ee
# class PostMutation(DjangoModelFormMutation):
#     post = graphene.Field(PostType)
#
#     class Meta:
#         form_class = PostForm
#
#
# class PostMutation(graphene.ObjectType):
#     create_post = PostMutation.Field()
#     update_post = PostMutation.Field()


class CreatePost(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    data = graphene.Field(PostType)

    class Arguments:
        input = PostInput(required=True)

    @classmethod
    @login_required
    @permission_required("db.create_post")
    def mutate(cls, root, info, input, **kwargs):
        post = Post()
        post.name = input.name
        post.text = input.text
        post.image = input.image
        post.category_id = input.category_id
        post.written_by_id = info.context.user.id
        post.save()
        post.keywords.set(input.keywords)
        return CreatePost(success=True, errors=None, data=post)


class UpdatePost(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    data = graphene.Field(PostType)

    class Arguments:
        id = graphene.ID(required=True)
        input = PostInput(required=True)

    @classmethod
    @login_required
    @permission_required("db.update_post")
    def mutate(cls, root, info, id, input, **kwargs):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise Exception('Post Not Found')

        if post.written_by != info.context.user:
            raise Exception('Forbidden')

        post.name = input.name
        post.text = input.text
        post.image = input.image
        post.category_id = input.category_id
        post.save()
        post.keywords.set(input.keywords)
        return UpdatePost(success=True, errors=None, data=post)


class UploadPostImage(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        id = graphene.ID(required=True)
        image = Upload(required=True)

    @classmethod
    @login_required
    @permission_required("db.update_post")
    def mutate(cls, root, info, image, id=None, **kwargs):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise Exception('Post Not Found')

        if post.written_by != info.context.user:
            raise Exception('Forbidden')

        try:
            image_to_verify = Image.open(image)
            image_to_verify.verify()
        except Exception:
            raise Exception('No Image provided')

        try:
            post.image.save(image.name, image.file)
        except Exception as e:
            return UploadPostImage(success=False, errors=[str(e)])

        return UploadPostImage(success=True, errors=None)


class PostMutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    upload_post_image = UploadPostImage.Field()


class JwtMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token = graphql_jwt.DeleteJSONWebTokenCookie.Field()

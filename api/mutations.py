import graphene
import graphql_jwt
from graphql_jwt.decorators import permission_required, login_required
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_file_upload.scalars import Upload
from PIL import Image

from api.errors import GraphqlOutput, non_field_error
from api.forms import PostForm, CategoryForm, KeywordForm
from api.inputs import PostInput
from api.types import PostType, CategoryType
from db.models import Post


# Django Form
# Create Mode: no `id`
# Update Mode: provide `id` of record to update
class CategoryFormMutation(DjangoModelFormMutation):
    category = graphene.Field(CategoryType)

    class Meta:
        form_class = CategoryForm

    @classmethod
    @login_required
    @permission_required("db.update_category")
    def mutate(cls, root, info, input, **kwargs):
        return super().mutate(root, info, input)


class KeywordFormMutation(DjangoModelFormMutation):
    keyword = graphene.Field(CategoryType)

    class Meta:
        form_class = KeywordForm

    @classmethod
    @login_required
    @permission_required("db.update_keyword")
    def mutate(cls, root, info, input, **kwargs):
        return super().mutate(root, info, input)


# Manual with Forms
class UpdatePost(GraphqlOutput, graphene.Mutation):
    form_data = graphene.Field(PostType)

    class Arguments:
        id = graphene.ID()
        post = PostInput(required=True)

    @classmethod
    @login_required
    @permission_required("db.update_post")
    def mutate(cls, root, info, id, post, **kwargs):
        errors = {}
        user = info.context.user
        post_item = Post.objects.get(pk=id)
        try:
            if post_item.written_by != user.id and not user.is_superuser:
                return UpdatePost(success=False, errors=non_field_error('Cannot update posts of other users'))

            # manually set owner of post
            post['written_by'] = post_item.written_by_id

            form = PostForm(instance=post_item, data=post)
            if form.is_valid():
                form.save()
                return UpdatePost(success=True, form_data=form.instance)
            errors.update(form.errors.get_json_data())
            return UpdatePost(success=False, errors=errors)
        except BaseException:
            message = 'Error while trying to update post'
            errors.update(non_field_error(message))
            return UpdatePost(success=False, errors=errors)


class CreatePost(GraphqlOutput, graphene.Mutation):
    form_data = graphene.Field(PostType)

    class Arguments:
        post = PostInput(required=True)

    @classmethod
    @login_required
    @permission_required("db.create_post")
    def mutate(cls, root, info, post, **kwargs):
        errors = {}
        user = info.context.user
        try:
            # set owner
            post['written_by'] = user.id

            form = PostForm(data=post)
            if form.is_valid():
                form.save()
                return CreatePost(success=True, form_data=form.instance)
            errors.update(form.errors.get_json_data())
            return CreatePost(success=False, errors=errors)
        except BaseException:
            message = 'Error while trying to create post'
            errors.update(non_field_error(message))
            return CreatePost(success=False, errors=errors)


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

        if post.written_by != info.context.user and not info.context.user.is_superuser:
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


class CategoryMutation(graphene.ObjectType):
    create_category = CategoryFormMutation.Field()
    update_category = CategoryFormMutation.Field()


class KeywordMutation(graphene.ObjectType):
    create_keyword = KeywordFormMutation.Field()
    update_keyword = KeywordFormMutation.Field()


class JwtMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token = graphql_jwt.DeleteJSONWebTokenCookie.Field()

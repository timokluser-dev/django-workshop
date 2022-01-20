import graphene
import graphql_jwt
from graphene_django.types import ErrorType
from graphql_jwt.decorators import permission_required, login_required
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_file_upload.scalars import Upload
from PIL import Image

from api.errors import NoUpdatePostPermissionError, NoCreatePostPermissionError, NotYourPostError
from api.forms import PostForm
from api.types import PostType
from db.models import Post


# Django Form
class PostMutation(DjangoModelFormMutation):
    post = graphene.Field(PostType)
    errors = graphene.List(ErrorType)

    class Meta:
        form_class = PostForm

    @classmethod
    @login_required
    def mutate(cls, root, info, input, **kwargs):
        if input.id:
            if not info.context.user.has_perm('db.update_post') and not info.context.user.is_superuser:
                return cls(
                    errors=(
                        NoUpdatePostPermissionError(field='post',
                                                    messages=("you don't have permission to update posts",)),
                    )
                )
        else:
            if not info.context.user.has_perm('db.create_post'):
                return cls(
                    errors=(
                        NoCreatePostPermissionError(field='post',
                                                    messages=("you don't have permission to create posts",)),
                    )
                )

        if int(input.written_by) != info.context.user.id and not info.context.user.is_superuser:
            return cls(
                errors=(
                    NotYourPostError(field='writtenBy', messages=('you can only create and update your own posts',)),
                )
            )

        return super().mutate(root, info, input)


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
    create_post = PostMutation.Field()
    update_post = PostMutation.Field()
    upload_post_image = UploadPostImage.Field()


class JwtMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token = graphql_jwt.DeleteJSONWebTokenCookie.Field()

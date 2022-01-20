from graphene_django.types import ErrorType


# Information:
# ErrorType: errors -> __typename

class NoUpdatePostPermissionError(ErrorType):
    pass


class NoCreatePostPermissionError(ErrorType):
    pass


class NotYourPostError(ErrorType):
    pass

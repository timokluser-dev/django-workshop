import graphene
from graphene_django.utils import camelize


class GraphqlError(graphene.Scalar):
    class Meta:
        description = """
    Errors messages and codes mapped to
    fields or non fields errors.
    Example:
    {
        field_name: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        other_field: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        nonFieldErrors: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ]
    }
    """

    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        if isinstance(errors, list):
            return {"nonFieldErrors": errors}
        raise Exception("`errors` must be list or dict!")


class GraphqlOutput:
    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(GraphqlError)


def non_field_error(message):
    return [message]

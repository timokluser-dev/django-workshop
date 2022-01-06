import graphene


class PostInput(graphene.InputObjectType):
    name = graphene.String()
    text = graphene.String()
    image = graphene.String()
    category_id = graphene.ID()
    keywords = graphene.List(graphene.ID)

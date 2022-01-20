import graphene


class PostInput(graphene.InputObjectType):
    name = graphene.String()
    text = graphene.String()
    image = graphene.String()
    category = graphene.ID()
    keywords = graphene.List(graphene.ID)

import graphene
from api.queries import HelloQuery, CategoryQuery, KeywordQuery, PostQuery, UserQuery
from api.mutations import PostMutation


# general Query class
# all graphql as parent class
# first class has most weight in inheritance (e.g. if method multiple times)
class Query(HelloQuery, CategoryQuery, KeywordQuery, PostQuery, UserQuery):
    pass


class Mutation(PostMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene
from api.queries import HelloQuery, CategoryQuery, KeywordQuery, PostQuery, UserQuery
from api.mutations import PostMutation, JwtMutation, CategoryMutation, KeywordMutation


# general Query class
# all graphql as parent class
# first class has most weight in inheritance (e.g. if method multiple times)
class Query(HelloQuery, CategoryQuery, KeywordQuery, PostQuery, UserQuery):
    class Meta:
        description = 'Queries for fetching data'


class Mutation(PostMutation, CategoryMutation, KeywordMutation, JwtMutation):
    class Meta:
        description = 'Mutations for manipulating data'


schema = graphene.Schema(query=Query, mutation=Mutation)

import graphene

import cookbook.ingredients.schema.internalQuery
import cookbook.ingredients.schema.internalMutation

from cookbook.ingredients.schema.internalMutation import \
    CreateCategoryMutation, \
    UpdateCategoryMutation, \
    DeleteCategoryMutation, \
    CreateIngredientMutation, \
    UpdateIngredientMutation, \
    DeleteIngredientMutation

class Query(cookbook.ingredients.schema.internalQuery.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(graphene.ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()
    create_ingredient = CreateIngredientMutation.Field()
    update_ingredient = UpdateIngredientMutation.Field()
    delete_ingredient = DeleteIngredientMutation.Field()


schema = graphene.Schema(query=Query, mutation = Mutation)
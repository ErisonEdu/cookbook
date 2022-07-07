from select import select
from unicodedata import category
import graphene

from graphene_django.types import DjangoObjectType

from cookbook.ingredients.schema.internalQuery import CategoryNode
from ..models import Ingredient, Category

class IngredientType(DjangoObjectType):
    class Meta: 
        model = Ingredient
        fields = ("__all__")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("__all__")

class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)

class IngredientInput(graphene.InputObjectType):
    ingredient_id = graphene.Int()
    ingredient_name = graphene.String(required=True)
    ingredient_notes = graphene.String(required=True)
    ingredient_category = graphene.Int(required=True)

class CreateIngredientMutation(graphene.Mutation):
    class Arguments:
        ingredient_data = IngredientInput(required=True)

    ingredient = graphene.Field(IngredientType)

    @classmethod
    def mutate(cls, root, info, ingredient_data):
        category_obj = Category.objects.get(id = ingredient_data.ingredient_category)
        ingredient = Ingredient.objects.create(
            ingredient_name = ingredient_data.ingredient_name,
            notes = ingredient_data.ingredient_notes,
            category = category_obj
        )
        return CreateIngredientMutation(ingredient = ingredient)

class UpdateIngredientMutation(graphene.Mutation):
    class Arguments:
        ingredient_data = IngredientInput(required=True)

    ingredient = graphene.Field(IngredientType)

    @classmethod
    def mutate(cls, rooot, info, ingredient_data):
        category_obj = Category.objects.get(id = ingredient_data.ingredient_category)
        ingredient = Ingredient.objects.filter(id = ingredient_data.ingredient_id).first()
        ingredient.ingredient_name = ingredient_data.ingredient_name
        ingredient.notes = ingredient_data.ingredient_notes
        ingredient.category = category_obj
        ingredient.save()
        return UpdateIngredientMutation(ingredient = ingredient)

class DeleteIngredientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    msg = graphene.String()
    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    @classmethod
    def mutate(cls, root, info, id):
        ingredient = Ingredient.objects.get(id=id)
        ingredient.delete()
        return cls(msg = f'deleted item: {id}', ok = True)

class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        category_name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, category_name):
        category = Category(category_name = category_name)
        category.save()
        return CreateCategoryMutation(category = category)

class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        category_name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, category_name, id):
        category = Category.objects.get(id=id)
        category.category_name = category_name
        category.save()
        return UpdateCategoryMutation(category = category)

class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    msg = graphene.String()
    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return cls(msg = f'deleted item: {id}', ok = True)

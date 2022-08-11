from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphene

from blog import models

# class UserType(DjangoObjectType):
#     class Meta:
#         model = get_user_model()

# class AuthorType(DjangoObjectType):
#     class Meta:
#         model = models.Profile

class PostType(DjangoObjectType):
    class Meta:
        model = models.Post

class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    def resolve_all_posts(root, info):
        return (
            models.Post.objects.prefetch_related("tags").all()
        )

    def resolve_post_by_slug(root, info, slug):
        return (
            models.Post.objects.prefetch_related("tags").get(slug=slug)
        )

    def resolve_posts_by_tag(root, info, tag):
        return (
            models.Post.objects.prefetch_related("tags").filter(tags__name__iexact=tag)
        )
schema = graphene.Schema(query=Query)

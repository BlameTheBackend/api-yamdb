from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)
from .constants import API_VERSION


api_v1_router = routers.DefaultRouter()
api_v1_router.register('categories', CategoryViewSet)
api_v1_router.register('genres', GenreViewSet)
api_v1_router.register('titles', TitleViewSet)
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path(API_VERSION, include(api_v1_router.urls))
]

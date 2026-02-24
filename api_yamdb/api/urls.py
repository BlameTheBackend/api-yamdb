from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .constants import API_VERSION


api_v1_router = routers.DefaultRouter()
api_v1_router.register('categories', CategoryViewSet)
api_v1_router.register('genres', GenreViewSet)
api_v1_router.register('titles', TitleViewSet)

urlpatterns = [
    path(API_VERSION, include(api_v1_router.urls))
]

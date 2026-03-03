from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .constants import API_VERSION
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    SignupView,
    TokenView
)


api_v1_router = DefaultRouter()
api_v1_router.register('users', UserViewSet)
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
    path(
        f'{API_VERSION}auth/signup/',
        SignupView.as_view(),
        name='auth_signup'
    ),
    path(f'{API_VERSION}auth/token/', TokenView.as_view(), name='auth_token'),
    path(API_VERSION, include(api_v1_router.urls))
]

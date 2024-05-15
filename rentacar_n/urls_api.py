from django.urls import include, path
from rest_framework import routers

from core import views_rest

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path("add_user/", views_rest.UserCreateView.as_view()),
    path('users/', views_rest.UserListAPIviews.as_view()),
    path('users/<int:pk>/', views_rest.UserDetailAPIviews.as_view()),
]

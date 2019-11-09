from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipeapp import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipeapp'

urlpatterns = [
    path('', include(router.urls))
]
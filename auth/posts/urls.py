from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowPostsViewSet 

router = DefaultRouter()
router.register(r'posts', ShowPostsViewSet, basename='post') 

urlpatterns = [
    path('', include(router.urls)), 
]
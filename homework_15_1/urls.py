from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

from .models import TaskListAPIView, CategoryListAPIView
from .views import JSONFileAPIView, TextProcessingAPIView


router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('json/', JSONFileAPIView.as_view(), name='json_file_api'),
    path('text/', TextProcessingAPIView.as_view(), name='text_processing_api'),
    path('tasks/', TaskListAPIView.as_view(), name='task_list'),
    path('categories/', CategoryListAPIView.as_view(), name='category_list'),
]


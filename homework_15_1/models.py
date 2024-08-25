from django.db import models

# Create your models here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from task_manager_hw14.models import Task, Category
from task_manager_hw14.serializers import TaskSerializer, CategorySerializer

class TaskListAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
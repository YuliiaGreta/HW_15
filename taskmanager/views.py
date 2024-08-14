from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics
from .models import Task, SubTask  # Добавляем импорт модели SubTask
from .serializers import TaskSerializer, SubTaskCreateSerializer  # Добавляем импорт SubTaskCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Эндпойнт для создания задачи
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# Эндпойнт для получения списка задач с фильтрами и пагинацией
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    ordering_fields = ['deadline']
    ordering = ['deadline']

# Эндпойнт для получения статистики задач
class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        status_counts = Task.objects.values('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=timezone.now(), status__in=['pending', 'in_progress']).count()

        return Response({
            'total_tasks': total_tasks,
            'status_counts': status_counts,
            'overdue_tasks': overdue_tasks,
        })

# Новый эндпойнт для создания и получения списка подзадач
class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()  # Получаем все подзадачи
        serializer = SubTaskCreateSerializer(subtasks, many=True)  # Преобразуем их в JSON
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)  # Преобразуем JSON в объект
        if serializer.is_valid():  # Проверка данных
            serializer.save()  # Сохранение подзадачи
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Новый эндпойнт для получения, обновления и удаления конкретной подзадачи
class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)  # Получаем подзадачу по ID
        except SubTask.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        subtask = self.get_object(pk)  # Получаем подзадачу
        serializer = SubTaskCreateSerializer(subtask)  # Преобразуем в JSON
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)  # Получаем подзадачу
        serializer = SubTaskCreateSerializer(subtask, data=request.data)  # Преобразуем данные из запроса
        if serializer.is_valid():  # Проверка данных
            serializer.save()  # Сохранение изменений
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)  # Получаем подзадачу
        subtask.delete()  # Удаляем подзадачу
        return Response(status=status.HTTP_204_NO_CONTENT)  # Возвращаем успешный статус
from rest_framework import serializers
from .models import Task, SubTask, Category
from datetime import datetime

# Сериализатор для Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']

# Сериализатор для создания SubTask
class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask  # используем модель SubTask
        fields = ['id', 'title', 'description', 'created_at', 'task']  # указываем поля
        read_only_fields = ['created_at']  # поле created_at доступно только для чтения

# Сериализатор для создания Category с проверкой уникальности
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # используем модель Category
        fields = ['id', 'title', 'description']  # указываем поля

    def create(self, validated_data):
        title = validated_data.get('title')
        if Category.objects.filter(title=title).exists():  # проверяем на наличие категории с таким же названием
            raise serializers.ValidationError('Category already exists')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        title = validated_data.get('title', instance.title)
        if Category.objects.filter(title=title).exclude(id=instance.id).exists():
            raise serializers.ValidationError('Category already exists')
        return super().update(instance, validated_data)

# Сериализатор для SubTask
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'created_at', 'task']

# Сериализатор для подробного отображения Task с вложенными SubTasks
class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)  # вложенный сериализатор для подзадач

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'subtasks']  # указываем поля, включая подзадачи

# Сериализатор для создания Task с валидацией поля deadline
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']

    def validate_deadline(self, value):
        if value < datetime.now().date():  # проверяем, чтобы дата не была в прошлом
            raise serializers.ValidationError('Deadline must be in the future')
        return value
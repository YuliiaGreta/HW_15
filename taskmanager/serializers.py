from rest_framework import serializers
from .models import Task, SubTask, Category
from datetime import datetime

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']

# Добавить SubTaskCreateSerializer задание 1 HW  12
class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask # использую модель SubTask
        fields = ['id', 'title', 'description', 'created_at', 'task'] #Указываю поля
        read_only_fields = ['created_at'] #Делаю это поле сreated_at доступным только для чтения

# Создание CategoryCreateSerializer с проверкой уникальности HW 12 numer 2
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category #исп.модель Сategory
        fields = ['id', 'title', 'description'] # Указала поля

def create(self, validated_data):
    title = validated_data.pop('title')
    if Category.objects.filter(title=title).exists(): # Проверяю на наличие кате-и с таким же названием
       raise serializers.ValidationError('Category already exists')
    return super(),create(validated_data)
def update(self, instance, validated_data):
    title = validated_data.get('title', instance.title)
    if Category.objects.filter(title=title).exclude(id=instance).exists():
        raise serializers.ValidationError('Category already exists')
    return super(),update(instance,validated_data)

# Создание вложенного сериализатора TaskDetailSerializer HW 12 - 3

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask #
        fields = ['id', 'title', 'description', 'created_at', 'task']

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True) # Вложен сериализатор для подзадач
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'deadline', 'subtasks') # Указ поля, включая подзадачи

# Валидация поля deadline в TaskCreateSerializer HW 12 - 4
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']  # Указываем поля

        def validate_deadline(self, value):
            if value < datetime.now().date():  # Проверяем, чтобы дата не была в прошлом
                raise serializers.ValidationError('Deadline must be in the future')
            return value
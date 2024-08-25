from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import os
from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer
from .utils import clean_text, remove_stop_words
from task_manager_hw14.models import Category, Task

def write_to_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def read_from_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



class JSONFileAPIView(APIView):

    def post(self, request):
        # Ожидаем, что в теле запроса придут данные JSON и имя файла
        data = request.data.get('data')
        filename = request.data.get('filename')

        if not data or not filename:
            return Response({"error": "Data and filename are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(filename, 'w') as f:
                json.dump(data, f)
            return Response({"message": "File written successfully."}, status=status.HTTP_201_CREATED)
        except TypeError:
            return Response({"error": "Invalid data type."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Ожидаем, что имя файла будет передано в качестве параметра запроса
        filename = request.query_params.get('filename')

        if not filename or not os.path.exists(filename):
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        with open(filename, 'r') as f:
            data = json.load(f)
        return Response(data, status=status.HTTP_200_OK)


class TextProcessingAPIView(APIView):

    def post(self, request):
        # Ожидаем текст и стоп-слова в теле запроса
        text = request.data.get('text')
        stop_words = request.data.get('stop_words', [])

        if not text:
            return Response({"error": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)

        cleaned_text = clean_text(text)
        processed_text = remove_stop_words(cleaned_text, stop_words)

        return Response({"cleaned_text": cleaned_text, "processed_text": processed_text}, status=status.HTTP_200_OK)
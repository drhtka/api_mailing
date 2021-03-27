from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
from notes.models import Note
from api.serializers import NoteSerializer



@api_view(['GET', 'POST'])
def notes_list(request ):# format=None для оторажения в формате json
    if request.method == 'GET': # если метод 
        notes = Note.objects.all() # выдать все
        serializer = NoteSerializer(notes, many=True) # серелизотр в переменную
        return Response(serializer.data) # передаем
    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)# передаем данные
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)# статус DRF
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def notes_detail(request, pk, format=None):
    try:
        note = Note.objects.get(pk=pk)
    except Note.DoesNotExist: # если ошибка
        return Response( status=status.HTTP_404_NOT_FOUND)# если тако записи нет вернуть статус DRF
    if request.method == 'GET': # если метод гет вернуть запись которую получили
        serializer = NoteSerializer(note) # many=True не надо потому что одна запись
        return Response(serializer.data) # веруть запись которую получили
    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data)# к записи подвязываем изменные данные из реквест
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
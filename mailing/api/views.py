from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from notes.models import Note

from api.serializers import NoteSerializer, ThinNoteSerializer, UserSerializer
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, 
    UpdateModelMixin, DestroyModelMixin)# миксины
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView # чтоб правильно работали миксины
from rest_framework.viewsets import ModelViewSet # объеденяет в себе все миксины
#from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly # запрет не авторизированным, вход только админам
from rest_framework.permissions import IsAdminUser # новых пользователей создат только админ
from .permissions import IsAuthorOrReadOnly # если не прошел аутентификацию только чтение
from django.contrib.auth import get_user_model

################# User

class UserViewSet(ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

################# api на миксинах 3 варианта
############## вариант 3 #######################

class NoteViewSet(ModelViewSet):
    # model = Note
    # queryset = model.objects.none()
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post']# по умолчанию доступны все методы, здесь можно указать то что надо
    # permission_classes = (IsAuthenticated,)



    def list(self, request, *args, **kwags):
        notes = Note.objects.all()
        # notes = Note.objects.filter(author=self.request.user) # если надо филтровать ситатьи по пользователю
        context = {'request': request}
        serializer = ThinNoteSerializer(notes, many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)# Автоматически подвязываем юзера к статье

############## вариант 2 #######################
# class NoteListView(ListCreateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

#     def list(self, request, *args, **kwags):
#         notes = Note.objects.all()
#         context = {'request': request}
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)

# class NoteDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

############## вариант 1 #######################
# class NoteListView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

#     def get(self, request, *args, **kwags):
#         self.serializer_class = ThinNoteSerializer
#         return self.list(request, *args, **kwags) # list перeопределяем из миксина ListModelMixin

#     def post(self, request, *args, **kwags):
#         return self.create(request, *args, **kwags) # create перeопределяем из миксина CreateModelMixin

################# api на миксинах конец 3 варианта

################# api на классах
# class NoteListView(APIView):
#     def get(self, request, format=None):
#         notes = Note.objects.all()
#         context = {'request': request}# чтобы пердать request, нужно только так
#         serializer = ThinNoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NoteDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Note.objects.get(pk=pk)
#         except Note.DoesNotExist:
#             return Response( status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, pk, format=None):
#         note = self.get_object(pk)# получаем запись по id
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         note = self.get_object(pk)# получаем запись по id
#         serializer = NoteSerializer(note, data=request.data)# data=request.data здесь данные послередактиования ппо api
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         note = self.get_object(pk)
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


################# api на функциях
# @api_view(['GET', 'POST'])
# def notes_list(request ):# format=None для оторажения в формате json
#     if request.method == 'GET': # если метод 
#         notes = Note.objects.all() # выдать все
#         serializer = NoteSerializer(notes, many=True) # серелизотр в переменную
#         return Response(serializer.data) # передаем
#     elif request.method == 'POST':
#         serializer = NoteSerializer(data=request.data)# передаем данные
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)# статус DRF
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def notes_detail(request, pk, format=None):
#     try:
#         note = Note.objects.get(pk=pk)
#     except Note.DoesNotExist: # если ошибка
#         return Response( status=status.HTTP_404_NOT_FOUND)# если тако записи нет вернуть статус DRF
#     if request.method == 'GET': # если метод гет вернуть запись которую получили
#         serializer = NoteSerializer(note) # many=True не надо потому что одна запись
#         return Response(serializer.data) # веруть запись которую получили
#     elif request.method == 'PUT':
#         serializer = NoteSerializer(note, data=request.data)# к записи подвязываем изменные данные из реквест
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
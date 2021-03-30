from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import *
#DefaultRouter
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')
router.register('users', UserViewSet, basename='users')
urlpatterns = router.urls

# urlpatterns = [
#     path('notes/', NoteListView.as_view(),  name='notes-list'),
#     path('notes/<int:pk>/', NoteDetailView.as_view(), name='notes-detail'),
#     # path('notes/', notes_list,  name='notes-list'),
#     # path('notes/<int:pk>/', notes_detail, name='notes-detail'),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns) #для вывода в json

# #перечисляем методы которые есть в класах и пригдяться в приложении
# notes_list = NoteViewSet.as_view({
#     'get': 'list',
#     'post': 'create'}
# )
# notes_detail = NoteViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# urlpatterns = [
#     path('notes/', notes_list,  name='notes-list'),
#     path('notes/<int:pk>/', notes_detail, name='notes-detail'),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)
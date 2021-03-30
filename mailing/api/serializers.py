from rest_framework.serializers import (IntegerField, CharField, Serializer, ModelSerializer, HyperlinkedIdentityField, SerializerMethodField)
from notes.models import Note
from django.contrib.auth import get_user_model

class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'email', 'password', 'name', 'admin')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)# модель определеана в мета клссе
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))# методом pop  выдергиваем пароль
        return super()(instance, validated_data)


class NoteSerializer(ModelSerializer):
    author = SerializerMethodField(read_only=True)# не отбражается выбрать автора

    def get_author(self, obj):
        return str(obj.author.email)# отбражается емаил

    class Meta:
        model = Note
        fields = '__all__'


class ThinNoteSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='notes-detail')# для передачи url в шаблон
    author = SerializerMethodField(read_only=True)# не отбражается выбрать автора

    def get_author(self, obj):
        return str(obj.author.email) # отбражается емаил

    class Meta:
        model = Note
        fields = ('id', 'title', 'url', 'author')

# class NoteSerializer(Serializer):
#     # выводим все
#     id = IntegerField(read_only=True)
#     title = CharField(required=True, max_length=250)
#     text = CharField(required=False, allow_blank=True)

#     def create(self, validated_data):
#         # добавляем
#         return Note.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         # обновляем
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance

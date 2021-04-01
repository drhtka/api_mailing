from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
#from django.db import models
from django.contrib.auth.hashers import make_password, identify_hasher
from django.db.models import (EmailField, CharField, BooleanField, DateTimeField) # ууказываем поляк какие надо вместо стандартной

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, full_name=None,
                    is_active=True, is_staff=None, is_admin=None):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('Пользователь должен иметь и-мэйл адрес')
        if not password:
            raise ValueError('Пользователь должен ввести пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password) # хеширует пароль
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                    is_staff=True, is_admin=True)
        return user
    
    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,    
                    is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    name = CharField(max_length=255, blank=True, null=True)
    full_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' # поле по куоторому происходит валидация при авторизации
    REQUIRED_FIELDS = []   # если пусто то никаких доп полей запрашивать не будет

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.name:
            return self.name
        return self.email# если нет имени вернуть емаил
    
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email# если нет имени вернуть емаил

    def has_perm(self, perm, obj=None):
        # чтоб можно было зайти работать в админке
        return True

    def has_module_perms(self, app_label):
        # чтоб можно было зайти работать в админке
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        # print(self.password)
        return self.admin

    def save(self, *args, **kwargs):
        try:
            _alg = identify_hasher(self.password)# если пароль захешированный мы идем дальше
        except ValueError:# если ошибка 
            self.password = make_password(self.password)# произойдёт перопрелеление пароля и хеширование
        # if not self.id and not self.staff and not self.admin:
        #     self.password = make_password(self.password)
        super().save(*args, **kwargs)# сохранение





 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, name, age, interests, password=None):
        if not name:
            raise ValueError('The Name field must be set')
        user = self.model(name=name, age=age, interests=interests)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, age, password=None):
        user = self.create_user(name, age, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False, default='default')
    age = models.IntegerField(blank=False, null=False, default=0)
    is_online = models.BooleanField(default=False)
    interests = models.JSONField(default=dict)

    objects = UserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['age', 'interests']

    def __str__(self):
        return self.name

class Chat(models.Model):
    name = models.CharField(max_length=255, default='chat room', unique=True)
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)


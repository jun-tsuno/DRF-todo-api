from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinLengthValidator

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Todo(models.Model):
  STATUS_CHOICES = (
    (1, 'Done'),
    (2, 'Doing'),
    (3, 'Undone'),
  )
  title = models.TextField(max_length=150, validators=[MinLengthValidator(1)])
  status = models.IntegerField(choices=STATUS_CHOICES)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='todo')

  def __str__(self):
      return self.title
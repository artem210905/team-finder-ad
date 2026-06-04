from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager
from .utils import generate_avatar


MAX_LENGTH_NAME = 124
MAX_LENGTH_PHONE = 12
MAX_LENGTH_ABOUT = 256


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=MAX_LENGTH_NAME, verbose_name="Имя")
    surname = models.CharField(max_length=MAX_LENGTH_NAME, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name="Аватар")
    phone = models.CharField(max_length=MAX_LENGTH_PHONE, verbose_name="Телефон")
    github_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на GitHub")
    about = models.TextField(max_length=MAX_LENGTH_ABOUT, blank=True, verbose_name="О себе")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Вариант 1 Избранные проекты
    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
        verbose_name="Избранные проекты"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        # Если аватарка не загружена пользователем, генерируем её
        if not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"

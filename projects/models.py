from django.conf import settings
from django.db import models


MAX_LENGTH_NAME = 200
MAX_LENGTH_STATUS = 6


class Project(models.Model):
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_OPEN, "Открыт"),
        (STATUS_CLOSED, "Закрыт"),
    )

    name = models.CharField(max_length=MAX_LENGTH_NAME, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание проекта")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор проекта"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на GitHub")
    status = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        verbose_name="Статус проекта"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="participated_projects",
        verbose_name="Участники проекта"
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    company = models.CharField("Организация", max_length=100, blank=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="authors/", blank=True)
    is_author = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={"slug": self.url})


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

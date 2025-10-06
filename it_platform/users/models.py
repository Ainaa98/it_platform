from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомдукураган колдонуучу модели, электрондук почта менен кирүү үчүн
    """
    email = models.EmailField(unique=True, verbose_name="Электрондук почта")
    username = models.CharField(max_length=150, unique=True, verbose_name="Колдонуучу аты")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Аты")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Фамилиясы")

    is_active = models.BooleanField(default=True, verbose_name="Активдүү")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперколдонуучу")

    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Кошулган датасы")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Акыркы кирүү")

    # Кастомдукураган менеджерди колдонуу
    objects = CustomUserManager()

    # Кириш талабы катары электрондук почтаны колдонуу
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Колдонуучу"
        verbose_name_plural = "Колдонуучулар"
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Колдонуучунун толук атын алуу
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Колдонуучунун кыска атын алуу
        """
        return self.username

    @property
    def is_admin(self):
        "Колдонуучу администраторбу?"
        return self.is_staff

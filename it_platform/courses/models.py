from django.db import models
from django.conf import settings
from django.utils import timezone


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Башталгыч'),
        ('intermediate', 'Орто'),
        ('advanced', 'Жогорку'),
    ]

    title = models.CharField(max_length=200, verbose_name="Курстун аталышы")
    description = models.TextField(verbose_name="Сүрөттөмө")
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner',
        verbose_name="Деңгээли"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Баасы"
    )
    duration_hours = models.PositiveIntegerField(
        default=0,
        verbose_name="Убактысы (саат)"
    )
    image = models.ImageField(
        upload_to='courses/images/',
        null=True,
        blank=True,
        verbose_name="Сүрөт"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активдүү")
    is_free = models.BooleanField(default=False, verbose_name="Акысыз")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Автор"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курстар"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )
    title = models.CharField(max_length=200, verbose_name="Сабақтын аталышы")
    content = models.TextField(verbose_name="Мазмуну")
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Видео ссылкасы"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Тәртиби")
    duration_minutes = models.PositiveIntegerField(
        default=0,
        verbose_name="Убактысы (мүнөт)"
    )
    is_published = models.BooleanField(default=True, verbose_name="Жарыяланган")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Сабақ"
        verbose_name_plural = "Сабактар"
        ordering = ['order', 'created_at']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Студент"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Курс"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, verbose_name="Бүтүргөн")
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Каттоо"
        verbose_name_plural = "Каттоолор"
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)
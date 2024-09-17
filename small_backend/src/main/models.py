from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from unidecode import unidecode
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .tasks import first_day_send
import logging

logger = logging.getLogger(__name__)
class City(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("City Name"))
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name=_("Slug"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")

    def save(self, *args, **kwargs):
        if not self.slug:  # Проверяем, если slug еще не установлен
            # Транслитерация кириллического названия в латиницу
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)


class ModerationForCity(models.Model):
    admin = models.ForeignKey(User, verbose_name=_('Access administrator'), on_delete=models.CASCADE, unique=True)
    city = models.ManyToManyField(City, null=True, verbose_name=_('City'), blank=True,
                                  related_name='moderation_for_city')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.admin}"

    class Meta:
        verbose_name = _("Moderation for City")
        verbose_name_plural = _("Moderation for Cities")


class Role(models.TextChoices):
    EMPLOYEE = 'employee', _("Employee")
    MENTOR = 'mentor', _("Mentor")
    MANAGER = 'manager', _("Manager")


class Department(models.TextChoices):
    PRODUCTION = 'sp', _("SP (Production)")
    SECURITY = 'sb', _("SB (Security)")
    STORES = 'stores', _("Stores")
    OFFICES = 'offices', _("Offices")


class CustomUser(models.Model):
    telegram_id = models.CharField(max_length=30, unique=True, verbose_name=_("Telegram ID"), null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name=_("First name"))
    last_name = models.CharField(max_length=50, verbose_name=_("Last Name"))
    phone_number = PhoneNumberField(unique=True, verbose_name=_("Phone Number"))
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        verbose_name=_("Role")
    )
    department = models.CharField(
        max_length=10,
        choices=Department.choices,
        default=Department.OFFICES,
        verbose_name=_("Department")
    )
    job_day = models.DateField(verbose_name=_("Job Day"), blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name=_("City"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Получение текущего времени с учетом временной зоны, установленной в Django (например, Asia/Qyzylorda)
        now = timezone.now()
        print(f"-------------------------------------------{now}")
        logger.debug(f"-------------------------------------------{now}")
        # Добавляем 180 секунд к текущему времени
        future_time = now + timedelta(seconds=30)
        logger.debug(f"-------------------------------------------{future_time}")
        print(f"-------------------------------------------{future_time}")
        # Отправляем задачу с использованием `future_time` как ETA (для отложенной задачи)
        #first_day_send.apply_async((self.first_name,), eta=future_time)
        first_day_send.delay(self.first_name)
        # Сохраняем запись
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Telegram bot User")
        verbose_name_plural = _("Telegram bot users")
        ordering = ['-created_at']
        indexes = [models.Index(fields=['telegram_id', 'role', 'department', 'job_day'])]

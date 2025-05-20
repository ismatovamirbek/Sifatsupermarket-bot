from django.db import models

class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username or self.telegram_id}"


class VacancyApplication(models.Model):
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True)
    sex = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    birthday = models.DateField()
    age = models.PositiveIntegerField()
    family = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    convicted = models.CharField(max_length=50)
    rus_lang = models.CharField(max_length=50)
    job = models.CharField(max_length=100)
    job_duration = models.CharField(max_length=50)
    previous_job = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=255, blank=True, null=True)
    military_certificate_id = models.CharField(max_length=255, blank=True, null=True)
    military_certificate_type = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

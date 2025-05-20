from django.contrib import admin
from .models import BotUser, VacancyApplication

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "username", "telegram_id", "created_at")
    search_fields = ("telegram_id", "first_name", "last_name", "username")
    list_filter = ("created_at", "username")

    def full_name(self, obj):
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip()
    full_name.short_description = "Full Name"


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ("fullname", "phone", "telegram_id", "created_at")
    search_fields = ("fullname", "phone", "telegram_id", "username")
    list_filter = ("created_at", "sex", "education", "location")

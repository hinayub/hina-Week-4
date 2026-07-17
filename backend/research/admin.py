from django.contrib import admin

from .models import ResearchQuery


@admin.register(ResearchQuery)
class ResearchQueryAdmin(admin.ModelAdmin):
    list_display = ("query", "created_at")
    search_fields = ("query", "answer")
    readonly_fields = ("created_at",)

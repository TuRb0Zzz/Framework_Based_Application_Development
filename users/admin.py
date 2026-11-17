from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "slug")
    search_fields = ("name", "email")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("slug",)
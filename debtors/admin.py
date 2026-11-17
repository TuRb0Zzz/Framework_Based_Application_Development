from django.contrib import admin
from .models import Debtor
from debts.models import Debt

class DebtInline(admin.TabularInline):
    model = Debt
    fields = ("amount", "issue_date", "status")
    extra = 0
    can_delete = False
    readonly_fields = ("amount", "issue_date", "status")

@admin.register(Debtor)
class DebtorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "slug")
    search_fields = ("name", "phone")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("slug",)
    inlines = (DebtInline,)
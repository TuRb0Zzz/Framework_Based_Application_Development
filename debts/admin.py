from django.contrib import admin
from django.db.models import Count, Q
from django.contrib import messages
from django.utils.html import format_html
from .models import Debt

@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ("id", "debtor", "amount", "issue_date", "status", "is_large", "site_link")
    list_display_links = ("id", "debtor")
    list_editable = ("status",)
    search_fields = ("debtor__name", "user__name")
    list_filter = ("status", "issue_date", "is_large")
    ordering = ("-issue_date",)
    list_per_page = 10
    date_hierarchy = "issue_date"
    autocomplete_fields = ("debtor", "user")
    readonly_fields = ("slug", "is_large", "site_link")
    list_select_related = ("debtor", "user")
    actions = ("mark_as_paid", "mark_as_active")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(active_debts=Count("debtor__debts", filter=Q(debtor__debts__status="active")))

    @admin.display(description="Страница на сайте")
    def site_link(self, obj):
        return format_html('<a href="{}" target="_blank">Открыть</a>', obj.get_absolute_url())

    @admin.action(description="Отметить как оплаченные")
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status="paid")
        self.message_user(request, f"Оплачено долгов: {updated}.", messages.SUCCESS)

    @admin.action(description="Вернуть в активные")
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status="active")
        self.message_user(request, f"Возвращено в активные: {updated}.", messages.SUCCESS)
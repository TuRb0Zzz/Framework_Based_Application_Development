from .models import Debt

def debt_context(request):
    return {
        "site_name": "Долговой трекер",
        "total_debts": Debt.objects.count(),
        "active_debts_count": Debt.objects.active().count(),
    }
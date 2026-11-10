from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from .models import Debt
from debtors.models import Debtor

def debt_list(request):
    debts = Debt.objects.select_related('debtor', 'user').all()
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    date_str = request.GET.get('date', '')
    error = None

    if query:
        debts = debts.filter(debtor__name__icontains=query)
    if status == 'paid':
        debts = debts.filter(is_paid=True)
    elif status == 'unpaid':
        debts = debts.exclude(is_paid=True)

    if date_str:
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            debts = debts.filter(issue_date=parsed_date)
        except ValueError:
            error = "Некорректный формат даты. Используйте ГГГГ-ММ-ДД."

    sort_by = request.GET.get('sort', 'date')
    sort_mapping = {
        'date': '-issue_date',
        'amount': 'amount',
        'debtor': 'debtor__name'
    }
    debts = debts.order_by(sort_mapping.get(sort_by, '-issue_date'))

    paginator = Paginator(debts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'debts': page_obj,
        'page_obj': page_obj,
        'query': query,
        'status': status,
        'date_str': date_str,
        'error': error,
        'sort_by': sort_by,
    }
    return render(request, 'debts/debt_list.html', context)

def debt_stats(request):
    debtors_stats = Debtor.objects.annotate(
        total_amount=Sum('debts__amount', filter=Q(debts__is_paid=False)),
        debt_count=Count('debts')
    ).order_by('-total_amount')

    total_all_debts = Debt.objects.aggregate(total=Sum('amount'))['total'] or 0
    unpaid_count = Debt.objects.filter(is_paid=False).count()

    context = {
        'statistics': debtors_stats,
        'total_all': total_all_debts,
        'unpaid_count': unpaid_count,
    }
    return render(request, 'debts/stats.html', context)

def debt_detail(request, debt_id):
    debt = get_object_or_404(Debt.objects.select_related('debtor', 'user'), pk=debt_id)
    return render(request, 'debts/debt_detail.html', {'debt': debt})

def search_debts(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Debt.objects.filter(
            debtor__name__icontains=query
        ).select_related('debtor')
    return render(request, 'debts/search.html', {'results': results, 'query': query})
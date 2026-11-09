from django.shortcuts import render
from db.database import get_connection

def debt_list(request):
    conn = get_connection()
    debts = conn.execute("""
        SELECT debts.id, debtors.name AS debtor_name, debts.amount, debts.is_paid
        FROM debts
        JOIN debtors ON debts.debtor_id = debtors.id
        ORDER BY debts.issue_date DESC
    """).fetchall()
    conn.close()
    return render(request, 'debts/debt_list.html', {'debts': debts})

def debt_stats(request):
    conn = get_connection()
    statistics = conn.execute("""
        SELECT debtors.name AS debtor_name, 
               COUNT(debts.id) AS debt_count, 
               SUM(debts.amount) AS total_amount
        FROM debts
        JOIN debtors ON debts.debtor_id = debtors.id
        GROUP BY debtors.id, debtors.name
        ORDER BY total_amount DESC
    """).fetchall()
    conn.close()
    return render(request, 'debts/stats.html', {'statistics': statistics})

def search_debts(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        conn = get_connection()
        results = conn.execute("""
            SELECT debts.id, debtors.name AS debtor_name, debts.amount, debts.is_paid
            FROM debts
            JOIN debtors ON debts.debtor_id = debtors.id
            WHERE debtors.name LIKE ?
        """, (f'%{query}%',)).fetchall()
        conn.close()
    return render(request, 'debts/search.html', {'results': results, 'query': query})

def debt_detail(request, debt_id):
    conn = get_connection()
    debt = conn.execute("""
        SELECT debts.*, debtors.name AS debtor_name, users.name AS user_name
        FROM debts
        JOIN debtors ON debts.debtor_id = debtors.id
        JOIN users ON debts.user_id = users.id
        WHERE debts.id = ?
    """, (debt_id,)).fetchone()
    conn.close()
    if not debt:
        return render(request, 'debts/debt_detail.html', {'error': 'Долг не найден'}, status=404)
    return render(request, 'debts/debt_detail.html', {'debt': debt})
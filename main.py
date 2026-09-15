from datetime import date, timedelta

def add_debt(debt_name, amount, due_date):
    return (f"Долг «{debt_name}» на сумму {amount:.2f} руб добавлен. Срок оплаты: {due_date.strftime('%d.%m.%Y')}")

def check_payment_reminder(due_date, today):
    days_left = (due_date - today).days
    if days_left < 0:
        return f"Внимание! Просрочка {abs(days_left)} дн. Необходимо срочно оплатить."
    elif days_left == 0:
        return "Сегодня последний день оплаты!"
    elif days_left <= 3:
        return f"Скоро оплата! Осталось {days_left} дн."
    else:
        return f"Оплата не требуется. До срока ещё {days_left} дн."

def calculate_payment_schedule(amount, months):
    if months <= 0:
        return "Ошибка: срок должен быть больше 0 месяцев."
    monthly_payment = amount / months
    return (f"График платежей: {months} мес. Ежемесячный платёж: {monthly_payment:.2f} руб.")

print("=== Сервис учёта долгов ===")
user_name = input("Введите ваше имя: ")
debt_name = input("Название долга: ")
amount_str = input("Сумма долга (руб.): ")
months_str = input("Срок в месяцах: ")

amount = float(amount_str)
months = int(months_str)

if amount <= 0:
    print("Ошибка: сумма долга должна быть положительной.")
else:
    today = date.today()
    due_date = today + timedelta(days=months * 30)

    print("\n--- Результаты ---")
    print(f"Пользователь: {user_name}")
    print(add_debt(debt_name, amount, due_date))
    print(check_payment_reminder(due_date, today))
    print(calculate_payment_schedule(amount, months))

    total_debt = amount
    print(f"Текущая сумма всех долгов: {total_debt:.2f} руб.")
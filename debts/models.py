from django.db import models
from users.models import User
from debtors.models import Debtor

class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="debts", verbose_name="Кредитор")
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name="debts", verbose_name="Должник")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачен")

    def __str__(self):
        return f"{self.debtor.name} - {self.amount} руб."

    class Meta:
        ordering = ["-issue_date"]
        verbose_name = "Долг"
        verbose_name_plural = "Долги"
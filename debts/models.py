from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
from users.models import User
from debtors.models import Debtor

class DebtQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)
    
    def paid(self):
        return self.filter(status=self.model.Status.PAID)
    
    def overdue(self):
        return self.filter(status=self.model.Status.OVERDUE)

class DebtManager(models.Manager.from_queryset(DebtQuerySet)):
    pass

class Debt(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        PAID = "paid", "Оплачен"
        OVERDUE = "overdue", "Просрочен"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="debts", verbose_name="Кредитор")
    debtor = models.ForeignKey(Debtor, on_delete=models.PROTECT, related_name="debts", verbose_name="Должник")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    issue_date = models.DateField(verbose_name="Дата выдачи")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ACTIVE, verbose_name="Статус")
    slug = models.SlugField(max_length=250, unique=True, blank=True, editable=False)
    
    is_large = models.GeneratedField(
        expression=models.Case(
            models.When(amount__gte=10000, then=models.Value(True)),
            default=models.Value(False),
            output_field=models.BooleanField()
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Крупный долг"
    )

    objects = DebtManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated = unidecode(f"{self.debtor.name}-{self.amount}")
            base_slug = slugify(transliterated) or "debt"
            slug = base_slug
            counter = 1
            while Debt.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("debts:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.debtor.name} - {self.amount} руб. ({self.get_status_display()})"

    class Meta:
        ordering = ["-issue_date"]
        verbose_name = "Долг"
        verbose_name_plural = "Долги"
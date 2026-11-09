from django.db import models

class Debtor(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должник"
        verbose_name_plural = "Должники"
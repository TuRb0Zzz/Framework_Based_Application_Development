from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кредитор"
        verbose_name_plural = "Кредиторы"
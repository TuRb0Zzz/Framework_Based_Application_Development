from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

class Debtor(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated = unidecode(self.name)
            base_slug = slugify(transliterated) or "debtor"
            slug = base_slug
            counter = 1
            while Debtor.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("debts:debtor_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должник"
        verbose_name_plural = "Должники"
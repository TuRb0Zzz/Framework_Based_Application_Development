from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

class User(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated = unidecode(self.name)
            base_slug = slugify(transliterated) or "user"
            slug = base_slug
            counter = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("debts:list")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кредитор"
        verbose_name_plural = "Кредиторы"
from django.db import models

from apps.menu.models.menu import Menu
from apps.taggit_autocomplete.managers import TaggableManager


class Meal(models.Model):
    menu = models.ForeignKey(Menu, related_name="meal")
    image = models.ImageField(null=True, blank=True)
    title = models.CharField("Title", max_length=255)
    price = models.FloatField("Price")
    tags = TaggableManager("Ingredients")
    order_count = models.PositiveIntegerField("Order count", default=0)

    class Meta:
        verbose_name = "Meal"
        verbose_name_plural = "Meal"
        ordering = ["title"]

    def __str__(self):
        return self.title

from django.db import models

from apps.core.models import BaseModel
from apps.restaurant.models import Restaurant


class Menu(BaseModel):
    title = models.CharField("Title", max_length=255)
    description = models.TextField("Description")
    restaurant = models.ForeignKey(Restaurant, related_name="menu")

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menu"

    def __str__(self):
        return self.title

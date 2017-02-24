from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.account.models import City
from apps.core.models import BaseModel


class Restaurant(BaseModel):
    title = models.CharField("Title", max_length=255)
    description = models.TextField("Description")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    city = models.ForeignKey(City)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("restaurant", kwargs={"pk": self.id})

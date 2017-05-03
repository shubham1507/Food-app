from django.conf import settings
from django.db import models
from django.db.models import Sum, F, Avg, FloatField
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

    def rating(self):
        return self.review_set.aggregate(rate=Avg(F('rate'), output_field=FloatField()))


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    rate = models.IntegerField(choices=[(x, str(x)) for x in range(1, 6)], default=5)
    restaurant = models.ForeignKey(Restaurant)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ["author", "restaurant"]
        ordering = ["-created_at"]

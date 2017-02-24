from django.conf import settings
from django.db import models

from apps.restaurant.models import Restaurant


class Order(models.Model):
    ORDER_STATUS = [("new", "New",), ("finalized", "Finalized",), ("rejected", "Rejected",)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    restaurant = models.ForeignKey(Restaurant)
    meal_name = models.CharField("Meal", max_length=255)
    meal_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS, default="new", max_length=100)

    def __str__(self):
        return "%s [%s]" % (self.meal_name, self.status)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

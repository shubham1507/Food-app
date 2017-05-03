import json
from datetime import timedelta

from django.utils import timezone

from channels import Group
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.restaurant.models import Restaurant


def order_time():
    return timezone.now() + timedelta(hours=1)


class Coupon(models.Model):
    code = models.CharField(max_length=255, unique=True)
    discount = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"


class Order(models.Model):
    CANCELLED_BY_CLIENT = "cancelled_by_client"
    NEW = "new"
    ORDER_STATUS = [(NEW, "New",), ("finalized", "Finalized",), ("rejected", "Rejected",),
                    (CANCELLED_BY_CLIENT, "Cancelled by client",)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    restaurant = models.ForeignKey(Restaurant)
    meal_name = models.CharField("Meal", max_length=255)
    coupon = models.ManyToManyField(Coupon, through='CouponUsed', blank=True, null=True)
    meal_price = models.FloatField()
    order_time = models.DateTimeField(default=order_time)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS, default="new", max_length=100)

    def __str__(self):
        return "%s [%s]" % (self.meal_name, self.id)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"


@receiver(post_save, sender=Order)
def update_stock(sender, instance, **kwargs):
    if instance.status != "new":
        Group("user-%s" % instance.user.id).send(
            content={"text": json.dumps({"id": instance.id, "status": instance.status, "name": instance.meal_name})},
            immediately=True)


class CouponUsed(models.Model):
    coupon = models.ForeignKey(Coupon)
    order = models.ForeignKey(Order)
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

from django.contrib import admin
from nested_admin.nested import NestedTabularInline, NestedStackedInline, NestedModelAdmin

from apps.menu.models.meal import Meal
from apps.menu.models.menu import Menu
from apps.order.models import Order
from apps.restaurant.forms import MealForm
from apps.restaurant.models import Restaurant


class MealInlineAdmin(NestedTabularInline):
    model = Meal
    extra = 1
    form = MealForm


class MenuInlineAdmin(NestedStackedInline):
    model = Menu
    extra = 0
    inlines = (MealInlineAdmin,)


class OrderInlineAdmin(NestedTabularInline):
    model = Order
    extra = 0
    readonly_fields = ["user", "meal_name", "meal_price", "order_time"]
    fields = ["user", "order_time", "meal_name", "meal_price", "status"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Restaurant)
class RestaurantAdmin(NestedModelAdmin):
    list_display = ("title", "city", "owner",)
    search_fields = list_display,
    list_filter = ("owner",)
    fields = ("title", "description", "city")
    inlines = (MenuInlineAdmin, OrderInlineAdmin,)

    class Media:
        js = ["https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js", "/static/website/js/select2.min.js",
              "/static/admin/js/admin.js"]
        css = {
            "all": ["/static/website/css/select2.min.css"]
        }

    def get_queryset(self, request):
        queryset = super(RestaurantAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(owner=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return []

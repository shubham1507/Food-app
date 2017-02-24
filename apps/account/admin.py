from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.account.models import User, City


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'city', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    class Media:
        js = ["https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js","/static/website/js/select2.min.js", "/static/admin/js/admin.js"]
        css = {
            "all": ["/static/website/css/select2.min.css"]
        }

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name"]

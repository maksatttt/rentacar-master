

# Register your models here.
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RentU, Cars, Orders


class RentUAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'lang')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email','lang', 'first_name', 'last_name', 'is_staff')

class CarsAdmin(admin.ModelAdmin):
    fields = ['name_car_en', 'foto', 'born_year', 'date_create']
    list_display = ('name_car_en', 'born_year', 'date_create')

class OrdersAdmin(admin.ModelAdmin):
    fields = ['renter', 'rented_car', 'date_begin', 'date_end', 'active']
    list_display = ('renter', 'rented_car', 'date_begin', 'date_end', 'active')

admin.site.register(RentU, RentUAdmin)
admin.site.register(Cars, CarsAdmin)
admin.site.register(Orders, OrdersAdmin)




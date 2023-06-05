from django.contrib import admin
from .models import Order
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number', 'date',)
    
    fields = ('order_number', 'date', 'full_name', 'email',
              'phone_number', 'country', 'postcode', 'tonw_or_city',
              'street_address1', 'street_address2', 'county', 'order_total',)

    list_display = ('order_number', 'date', 'full_name', 'order_total')

    ordering = ('-date',)

admin.sites.register(Order, OrderAdmin)


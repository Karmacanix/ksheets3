from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'city', 'country', 'business_name']
    search_fields = ['name', 'email', 'business_name']
    list_filter = ['city', 'country']

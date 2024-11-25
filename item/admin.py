from django.contrib import admin
from .models import Item, Cart

# Register your models here.

class ItemAdmin(admin.ModelAdmin):

    list_display = ['name', 'category', 'stock']
    list_display_links = ['name', 'category', 'stock']
    list_filter = ['category']
    search_fields = ['name']
    #list_editable = ['name', 'stock', 'category']

    class Meta:
        model = Item

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_name', 'cartnumber']
    class Meta:
        model = Cart

admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
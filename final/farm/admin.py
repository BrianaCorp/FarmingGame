from django.contrib import admin
from .models import Item, Plot, Points, InventoryItem

# Register your models here.
admin.site.register(Item)
admin.site.register(Plot)
admin.site.register(Points)
admin.site.register(InventoryItem)

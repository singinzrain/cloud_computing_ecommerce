from django.contrib import admin
from .models import User, Product, CartItem, Order

admin.site.register(User)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)

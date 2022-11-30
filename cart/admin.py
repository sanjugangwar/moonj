from django.contrib import admin
from .models import category,product,cart,trasaction,user_orders
# Register your models here.
admin.site.register(category)
admin.site.register(product)
admin.site.register(cart)
admin.site.register(trasaction)
admin.site.register(user_orders)
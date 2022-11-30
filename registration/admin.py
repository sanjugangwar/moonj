from django.contrib import admin
from .models import registration,login,Address


# Register your models here.

admin.site.register(registration)
admin.site.register(login)
admin.site.register(Address)

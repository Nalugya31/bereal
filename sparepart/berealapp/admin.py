from django.contrib import admin
from .models import *

# Register your models here.
# we register our models for the admin's use only.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Sale)
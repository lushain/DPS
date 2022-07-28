from django.contrib import admin
from .models import Invention, UserInvention
# Register your models here.

admin.site.register(Invention)
admin.site.register(UserInvention)

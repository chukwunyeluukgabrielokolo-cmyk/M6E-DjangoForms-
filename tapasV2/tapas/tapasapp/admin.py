from django.contrib import admin
from .models import Dish

# Register your models here.

class DishAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.account = request.user.account
        super().save_model(request, obj, form, change)
    
admin.site.register(Dish, DishAdmin)
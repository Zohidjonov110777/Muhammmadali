from django.contrib import admin
from .models import Category, Product, Profile, Order, ProductVariant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available']
    list_editable = ['price', 'available']

admin.site.register(ProductVariant)
admin.site.register(Profile)
admin.site.register(Order)
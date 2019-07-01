from django.contrib import admin
from store.models import Category, Product, ProductAttribute, Image, Order, Discount

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ProductAttribute)
admin.site.register(Image)
admin.site.register(Discount)




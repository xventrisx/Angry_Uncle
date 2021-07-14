from django.contrib import admin
from .models.staff import Staff
from .models.order import Product, Order, Score

#admin.site.register(Staff)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Score)


from django.contrib import admin
from .models import Business, BusinessProduct, BusinessNews
# Register your models here.
admin.site.register(Business)
admin.site.register(BusinessProduct)
admin.site.register(BusinessNews)

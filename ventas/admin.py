from django.contrib import admin

from ventas.models import *

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ( "id", "name", "dni", "type_dni", "address", "phone", "email", "user")
    search_fields = ('id','dni','name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "name", "price", "description", "id_publisher", "image","user")
    search_fields = ("key", "name")

class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "product")

class BildingAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "secuence","client")


class DetailBildingAdmin(admin.ModelAdmin):
    list_display = ("id", "price_unit", "amount", "bilding")

class CarShopAdmin(admin.ModelAdmin):
    list_display = ("id","amount","product")


class APIFaceModelAdmin(admin.ModelAdmin):
    list_display = ("id","token")

admin.site.register(APIFaceModel, APIFaceModelAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CatalogProduct, CatalogProductAdmin)
admin.site.register(Bilding, BildingAdmin)
admin.site.register(DetailBilding, DetailBildingAdmin)
admin.site.register(CarShop, CarShopAdmin)

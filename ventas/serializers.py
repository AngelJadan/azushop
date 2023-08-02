import random
from rest_framework import serializers
from ventas.models import Bilding, CarShop, CatalogProduct, Client, DetailBilding, Product

class ClientSerialiezer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields  = "__all__"

class CatalogProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogProduct
        fields = "__all__"
    
class ProductSerialiezer(serializers.ModelSerializer):
    product_catalog = CatalogProductSerializer(many=True, read_only=False)
    class Meta:
        model = Product
        fields = (
            "id",
            "key",
            "name",
            "price",
            "iva",
            "description",
            "id_publisher",
            "product_catalog"
        )

class CarShopReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarShop
        fields = "__all__"
        depth = 3

class CarShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarShop
        fields = "__all__"
    
    def update(self, CarShop, validated_data):
        CarShop.amount = validated_data.get("amount",CarShop.amount)
        CarShop.product = validated_data.get("product",CarShop.product)
        CarShop.client = validated_data.get("client", CarShop.client)
        return CarShop
class DetailBildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailBilding
        fields = "__all__"
        extra_kwargs ={"bilding":{"required":False,}}
        
class DetailBildingReadSerializer(serializers.ModelSerializer):
    product = ProductSerialiezer(many=False, read_only=True)
    class Meta:
        model = DetailBilding
        fields = ("id","price_unit","amount","product")
        depth = 2

        
class BildingReadSerializer(serializers.ModelSerializer):
    detail_bilding = DetailBildingReadSerializer(many=True, read_only=False)
    class Meta:
        model = Bilding
        fields = ("id", "date","secuence","client","detail_bilding")
        depth = 2

class BildingSerializer(serializers.ModelSerializer):
    detail_bilding = DetailBildingSerializer(many=True, read_only=False)
    class Meta:
        model = Bilding
        fields = (
            "date",
            "secuence",
            "client",
            "detail_bilding",
        )
        extra_kwargs = {
            "secuence":{"required":False}
        }
    
    def create(self, validated_data):
        details = validated_data.pop("detail_bilding")
        secuence_temp = validated_data.pop("secuence")
        client = validated_data.pop("client")
        dat = Bilding.objects.filter(client=client,secuence=secuence_temp)
        if len(dat)>0:
            secuence_temp = random.randrange(1, 999)
        new_bilding = Bilding.objects.create(
            **validated_data,
            secuence=secuence_temp,
            client=client
        )
        data_details =[]
        for detail in details:
            new_detail = DetailBilding.objects.create(**detail,bilding=new_bilding)
            data_details.append(new_detail)
        return new_bilding



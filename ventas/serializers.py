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
        fields = "__all__"

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

class BildingSerializer(serializers.ModelSerializer):
    detail_bilding = DetailBildingSerializer(many=True, read_only=False)
    class Meta:
        extra_kwargs = {
            "secuence":{"required":False}
        }
        model = Bilding
        fields = "__all__"
    
    def create(self, validated_data):
        details = validated_data.pop("detail_bilding")
        new_bilding = Bilding.objects.create(
            **validated_data
        )
        details =[]
        for detail in details:
            new_detail = DetailBilding.objects.create(**detail,bilding=new_bilding)
            details.append(new_detail)
        new_bilding.set(details)
        return new_bilding



from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class APIFaceModel(models.Model):
    id = models.AutoField(db_column="afa_id", db_index=True, primary_key=True, verbose_name="ID")
    token = models.CharField(db_column="afa_token", max_length=2000, verbose_name="API token")

    class Meta:
        verbose_name = "APIFacebook"
        verbose_name_plural = "APIFacebooks"

    def __str__(self):
        return f"{self.id}"
TYPE_DNI = (
    ("1","Cedula"),
    ("2","RUC"),
    ("3","Pasaporte"),
    ("4","Extranjero")
)

class Client(models.Model):
    id = models.AutoField(db_column="cli_id", db_index=True, primary_key=True, verbose_name="ID")
    name = models.CharField(db_column="cli_name", max_length=500, verbose_name="Name")
    dni = models.CharField(db_column="cli_dni", max_length=20, verbose_name="dni")
    type_dni = models.CharField(db_column="cli_type", max_length=2, verbose_name="TYPE_DNI")
    address = models.CharField(db_column="cli_address", max_length=500, verbose_name="Address")
    phone = models.CharField(db_column="cli_phone", max_length=20, verbose_name="Phone")
    email = models.EmailField(db_column="cli_email", max_length=1000, verbose_name="Email")
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.id}"

class Product(models.Model):
    IVA = (
        ("0","0%"),
        ("12","12%"),
    )
    id = models.AutoField(primary_key=True,db_index=True, db_column="pro_id", verbose_name="Id")
    key = models.CharField(db_column="pro_key", max_length=50, verbose_name="Key")
    name = models.CharField(db_column="pro_name", max_length=50, verbose_name="Name")
    price = models.FloatField(db_column="pro_price", verbose_name="Price")
    iva = models.CharField(db_column="pro_iva", max_length=2, choices=IVA, verbose_name="IVA")
    description = models.CharField(db_column="pro_description", verbose_name="Description")
    id_publisher = models.CharField(db_column="pro_publisher", max_length=500, null=True, blank=True, default=None,verbose_name="Publisher ID facebook")
    user = models.ForeignKey(User, db_column="pro_user", on_delete=models.CASCADE, verbose_name="User")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.id}"



class CatalogProduct(models.Model):
    id = models.AutoField(db_column="cat_id", db_index=True, primary_key=True)
    image = models.ImageField(db_column="cat_image", upload_to="images/")
    product = models.ForeignKey(Product, related_name="product_catalog", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Catalog"
        verbose_name_plural = "Catalogs"
    
    def __str__(self):
        return f"{self.id}"
    

class Bilding(models.Model):
    id = models.AutoField(db_column="bil_id", db_index=True,primary_key=True, verbose_name="Id")
    date = models.DateField(db_column="bil_date",auto_now_add=True, verbose_name="Date")
    secuence = models.IntegerField(db_column="bil_secuence", verbose_name="Secuence")
    client = models.ForeignKey(User, on_delete=models.CASCADE, db_column="bil_client",verbose_name="Client")
    
    class Meta:
        verbose_name = "Bilding"
        verbose_name_plural = "Bildings"
    
    def __str__(self):
        return f"{self.id}"

class DetailBilding(models.Model):
    id = models.AutoField(primary_key=True,db_column="dbi_id", db_index=True, verbose_name="ID")
    price_unit = models.FloatField(db_column="dbi_price_unit", verbose_name="Price unit")
    amount = models.FloatField(db_column="dbi_amount", verbose_name="Amount")
    bilding = models.ForeignKey(Bilding, db_column="dbi_bilding", related_name="detail_bilding", on_delete=models.CASCADE, verbose_name="Bilding")
    product = models.ForeignKey(Product, db_column="dbi_product",   related_name="detail_product", on_delete=models.CASCADE, verbose_name="Product")
    class Meta:
        verbose_name = "Detail bilding"
        verbose_name_plural = "Detail bildings"
    
    def __str__(self):
        return f"{self.id}"

class CarShop(models.Model):
    id = models.AutoField(primary_key=True, db_column="car_id", db_index=True, verbose_name="Id")
    amount = models.FloatField(db_column="car_amount", default=1, verbose_name="Amount")
    product = models.ForeignKey(Product,on_delete=models.CASCADE, db_column="car_product", verbose_name="Product")
    client = models.ForeignKey(User, on_delete=models.CASCADE, db_column="car_client", verbose_name="Client")

    class Meta:
        verbose_name = "Carshop"
        verbose_name_plural = "Carshop"

    def __str__(self):
        return f"{self.id}"

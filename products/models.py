from django.db import models

class Product(models.Model):
    korean_name       = models.CharField(max_length=50)
    english_name      = models.CharField(max_length=50)
    description       = models.CharField(max_length=1000)
    thumbnail_image   = models.CharField(max_length=1000)
    country_of_origin = models.CharField(max_length=50)
    material          = models.CharField(max_length=50)
    launched_at       = models.DateTimeField()

    class Meta:
        db_table = "products"

class ProductImage(models.Model):
    url     = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_images"

class Size(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "sizes"

class Color(models.Model):
    color = models.CharField(max_length=20)

    class Meta:
        db_table = "colors"

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)
    price   = models.DecimalField(max_digits=30, decimal_places=5)
    stock   = models.IntegerField()

    class Meta:
        db_table = "product_options"

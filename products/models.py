from django.db import models

class Product(models.Model):
    name              = models.CharField(max_length=50)
    quantity          = models.IntegerField()
    price             = models.DecimalField()
    description       = models.CharField(max_length=1000)
    thumbnail_image   = models.CharField(max_length=1000)
    country_of_origin = models.CharField(max_length=50)
    material          = models.CharField(max_length=50)
    launched_at       = models.DateTimeField()

    class Meta:
        db_tables = "products"

class ProductImage(models.Model):
    url     = models.CharField(max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_tables = "product_images"

class Size(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_tables = "sizes"

class Color(models.Model):
    color = models.CharField(max_length=20)

    class Meta:
        db_tables = "colors"

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)
    color   = models.ForeignKey(Color, on_delete=models.CASCADE)
    price   = models.DecimalField()
    stock   = models.IntegerField()

    class Meta:
        db_tables = "product_options"
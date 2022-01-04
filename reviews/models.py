from django.db import models

from users.models    import User
from products.models import Product

class Review(models.Model):
    user                 = models.ForeignKey(User, on_delete=models.CASCADE)
    product              = models.ForeignKey(Product, on_delete=models.CASCADE)
    star_point           = models.DecimalField(max_digits=5, decimal_places=1)
    size_information     = models.DecimalField(max_digits=5, decimal_places=1)
    color_information    = models.DecimalField(max_digits=5, decimal_places=1)
    quantity_information = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta:
        db_table = "review"

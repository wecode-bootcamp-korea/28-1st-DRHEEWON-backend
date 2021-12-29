from django.db import models

from users.models                import User
from products.models             import ProductOption
from dr_martens.time_stamp_model import TimeStampModel

class Cart(TimeStampModel):
    user            = models.ForeignKey(User, on_delete=CASCADE)
    product_option  = models.ForeignKey(ProductOption, on_delete=CASCADE)
    quantity        = models.IntegerField()

    class Meta:
        db_table = "carts"

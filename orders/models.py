from typing                      import Callable
from django.db                   import models
from django.db.models.deletion   import CASCADE
from dr_martens.time_stamp_model import TimeStampModel
from users.models                import User
from products.models             import ProductOption

class OrderStatus(models.Model):
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "order_statuses"

class Order(TimeStampModel):
    user         = models.ForeignKey(User, on_delete=CASCADE)
    order_number = models.CharField(max_length=30)
    order_status = models.ForeignKey(OrderStatus, on_delete=CASCADE)

    class Meta:
        db_table = "orders"

class OrderItem(TimeStampModel):
    product_option = models.ForeignKey(ProductOption, on_delete=CASCADE)
    quantity       = models.IntegerField()
    order          = models.ForeignKey(Order, on_delete=CASCADE)

    class Meta:
        db_table = "order_itmes"
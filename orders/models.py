import uuid

from django.db import models

from users.models                import User
from products.models             import ProductOption
from dr_martens.time_stamp_model import TimeStampModel

class OrderStatus(models.Model):
    status = models.CharField(max_length=30)

    class Meta:
        db_table = "order_statuses"

class Order(TimeStampModel):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.UUIDField(default=uuid.uuid4)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"

class OrderItem(TimeStampModel):
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    order          = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = "order_itmes"

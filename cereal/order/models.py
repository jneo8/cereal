from django.db import models

# Create your models here.


class Order(models.Model):
    """Order table."""
    id = models.IntegerField(primary_key=True)
    customer = models.IntegerField()  # may be fk.
    shipping = models.IntegerField()
    created_at = models.DateTimeField()


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300)

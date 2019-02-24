import logging
from datetime import datetime
from django.db import models

logger = logging.getLogger(__name__)

class Order(models.Model):
    """Order table."""

    def save(self, *args, **kwargs):

        # handle created_at
        created_at = self.created_at
        if "上午" in created_at or "下午" in created_at:
            if "上午" in created_at:
                created_at = created_at.replace("上午", "AM")
            if "下午" in created_at:
                created_at = created_at.replace("下午", "PM")
            created_at = datetime.strptime(created_at, "%Y/%m/%d %p %H:%M:%S")

        self.created_at = created_at


        super().save(*args, **kwargs)

    id = models.IntegerField(primary_key=True)
    customer = models.IntegerField()  # may be fk.
    shipping = models.IntegerField()
    created_at = models.DateTimeField()

    @classmethod
    def zero_shipping_pct(cls):
        """Return shipping equal to 0 %, return count."""
        pct = cls.objects.filter(shipping=0).count() / cls.objects.all().count()
        return [pct, 1 - pct]



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300)
    qty = models.IntegerField()

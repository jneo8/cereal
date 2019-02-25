import logging
from datetime import datetime, timedelta
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

    @classmethod
    def cohort_analysis(cls):
        """Return Cohort data.

        Note:
            This func may have performance issue if data size too big.
        """
        items = (
                cls
                .objects
                .extra(select={"day": "date( created_at )"})
                .values("day", "customer")
                .annotate(count=models.Count("id"))
                .order_by("day")
        )
        data = {}
        for item in items:
            logger.debug(item)
            if not data.get(item["day"]):
                data[item["day"]] = []
            data[item["day"]].append(item["customer"])

        days = []
        if len(data.keys()) > 0:
            first_day = datetime.strptime(list(data.keys())[0], "%Y-%m-%d").date()
            last_day = datetime.strptime(list(data.keys())[-1], "%Y-%m-%d").date()
            for day in (first_day + timedelta(days=n) for n in range((last_day - first_day).days + 1)):
                days.append(day)

        chart_data = []
        for idx_1, day_1 in enumerate(days):
            people = data.get(day_1.strftime("%Y-%m-%d"), [])
            for idx_2, day_2 in enumerate(days):
                value = 0
                if day_2 >= day_1:
                    p = data.get(day_2.strftime("%Y-%m-%d"), [])
                    if len(people) == 0 or len(p) == 0:
                        value = 0
                    else:
                        pct = len(set(people) & set(p)) / len(people)
                        pct = int(pct * 100)
                        value = pct
                chart_data.append([idx_1, idx_2, value])
        return {
            "days": [d.strftime("%Y-%m-%d") for d in days][::-1],
            "chart_data": chart_data,
        }


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=300)
    qty = models.IntegerField()

    @classmethod
    def hot_items(cls, size):
        """Return top size hot item."""
        items = cls.objects.values("product_name").annotate(product_count=models.Count("product_name")).order_by("-product_count")[:size]
        return items

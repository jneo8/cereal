import logging
import traceback
from django.core.management.base import BaseCommand, CommandError

import pandas as pd

from ...models import OrderItem, Order

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "import Order csv file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs="+", type=str)

    def handle(self, *args, **options):
        for file in options["file_path"]:
            try:
                df = pd.read_csv(file)
                for idx, row in df.iterrows():
                    order = Order.objects.get(id=row["order_id"])
                    order_item = OrderItem(
                        order=order,
                        product_name=row["product_name"],
                        qty=row["qty"],
                    )
                    order_item.save()
            except Exception as e:
                logger.error(traceback.format_exc())

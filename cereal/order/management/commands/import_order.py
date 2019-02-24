import logging
import traceback
from django.core.management.base import BaseCommand, CommandError

import pandas as pd

from ...models import Order

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
                    created_at = row["created_at"]
                    order = Order(
                        id=row["order_id"],
                        customer=row["customer_id"],
                        shipping=row["shipping"],
                        created_at=row["created_at"],
                    )
                    order.save()
                    logger.debug(row)
            except Exception as e:
                logger.error(traceback.format_exc())

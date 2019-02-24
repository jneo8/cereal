import logging
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "import Order csv file."

    def handle(self, *args, **options):
        logger.debug(args)
        logger.debug(options)

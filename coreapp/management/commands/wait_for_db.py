import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to make DB wait till it is available"""

    def handle(self, *args, **options):
        self.stdout.write("Checking database connection...")
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 sec...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
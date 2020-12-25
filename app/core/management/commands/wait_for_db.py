import time

from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand

class Command(BaseCommand):
    """
    Django command to pause database connection until is available
    """
    def handle(self, *args, **options):
        """
        Mathod for handling connection messages
        """
        self.stdout.write('Waiting for database connection')
        db_conn = None

        # Checking database connection
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database connection not available...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database online for transaction...'))
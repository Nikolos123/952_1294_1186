from django.core.management.base import BaseCommand
from django.utils.timezone import now

from mainapp.models import Product
from django.db.models import Q,F
from datetime import timedelta

from ordersapp.models import Order


class Command(BaseCommand):
   def handle(self, *args, **options):
       order = Order.objects.get(id=6)
       order.updated = now()+ timedelta(hours=12)
       order.save()



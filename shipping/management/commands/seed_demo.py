from django.core.management.base import BaseCommand

from shipping.models import Box, Order, OrderItem, Product

PRODUCTS = [
    ("BOOK", "Paperback book", 20, 15, 3, 0.5),
    ("ROD", "Fishing rod", 35, 5, 5, 1),
    ("MUG", "Ceramic mug", 10, 10, 12, 0.4),
    ("SHOE", "Shoe box", 33, 20, 12, 0.9),
    ("LAPTOP", "Laptop", 35, 25, 3, 1.8),
    ("ANVIL", "Anvil", 15, 15, 15, 50),
]
BOXES = [
    ("Small", 25, 20, 10, 5, 10),
    ("Medium", 40, 30, 30, 15, 20),
    ("Large", 60, 40, 40, 30, 35),
]


class Command(BaseCommand):
    help = "Load demo products, boxes and a sample order (safe to run repeatedly)."

    def handle(self, *args, **options):
        for sku, name, l, w, h, kg in PRODUCTS:
            Product.objects.update_or_create(sku=sku, defaults=dict(
                name=name, length_cm=l, width_cm=w, height_cm=h, weight_kg=kg))
        for name, l, w, h, kg, cost in BOXES:
            Box.objects.update_or_create(name=name, defaults=dict(
                inner_length_cm=l, inner_width_cm=w, inner_height_cm=h,
                max_weight_kg=kg, cost=cost, is_active=True))
        order, _ = Order.objects.get_or_create(reference="ORD-1001")
        for sku, qty in (("BOOK", 2), ("ROD", 1)):
            OrderItem.objects.update_or_create(
                order=order, product=Product.objects.get(sku=sku), defaults={"quantity": qty})
        self.stdout.write(self.style.SUCCESS("Demo data loaded."))

from django.db import models

# Create your models here.

from django.core.validators import MinValueValidator

POSITIVE = [MinValueValidator(0.01)]


class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=POSITIVE)
    width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=POSITIVE)
    height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=POSITIVE)
    weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Box(models.Model):
    name = models.CharField(max_length=100, unique=True)
    inner_length_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=POSITIVE)
    inner_width_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=POSITIVE)
    inner_height_cm = models.DecimalField(max_digits=8, decimal_places=2, validators=POSITIVE)
    max_weight_kg = models.DecimalField(max_digits=8, decimal_places=3, validators=POSITIVE)
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "boxes"

    def __str__(self):
        return self.name


class Order(models.Model):
    reference = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "product"], name="uniq_product_per_order"),
        ]

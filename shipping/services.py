from decimal import Decimal
from typing import Iterable, Tuple

from .models import Box, Product
from .packing import BoxSpec, Item, Recommendation, recommend_box

MAX_UNITS = 500  # guard against absurd requests


class InputError(ValueError):
    pass


def _f(d: Decimal) -> float:
    return float(d)


def items_from_lines(lines: Iterable[Tuple[Product, int]]):
    items = []
    for product, qty in lines:
        if qty < 1:
            raise InputError(f"Quantity for {product.sku} must be >= 1")
        for _ in range(qty):
            items.append(Item(_f(product.length_cm), _f(product.width_cm),
                              _f(product.height_cm), _f(product.weight_kg), product.sku))
        if len(items) > MAX_UNITS:
            raise InputError(f"Too many units (max {MAX_UNITS})")
    return items


def active_boxes():
    return [BoxSpec(b.id, b.name, _f(b.inner_length_cm), _f(b.inner_width_cm),
                    _f(b.inner_height_cm), _f(b.max_weight_kg), _f(b.cost))
            for b in Box.objects.filter(is_active=True)]


def recommend_for_lines(lines) -> Recommendation | None:
    return recommend_box(active_boxes(), items_from_lines(lines))

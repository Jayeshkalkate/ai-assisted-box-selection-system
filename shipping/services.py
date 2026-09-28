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
    lines = list(lines)
    for product, qty in lines:
        if qty < 1:
            raise InputError(f"Quantity for {product.sku} must be >= 1")
    # Check the total BEFORE expanding into individual units, otherwise a huge
    # quantity (e.g. 10**9) would try to allocate that many objects first.
    if sum(qty for _, qty in lines) > MAX_UNITS:
        raise InputError(f"Too many units (max {MAX_UNITS})")
    items = []
    for product, qty in lines:
        try:
            item = Item(_f(product.length_cm), _f(product.width_cm),
                        _f(product.height_cm), _f(product.weight_kg), product.sku)
        except ValueError as exc:  # bad data saved outside the admin forms
            raise InputError(str(exc)) from exc
        items.extend([item] * qty)  # Item is frozen/immutable, so sharing is safe
    return items


def active_boxes():
    boxes = []
    for b in Box.objects.filter(is_active=True):
        try:
            boxes.append(BoxSpec(b.id, b.name, _f(b.inner_length_cm), _f(b.inner_width_cm),
                                 _f(b.inner_height_cm), _f(b.max_weight_kg), _f(b.cost)))
        except ValueError:
            continue  # skip a box with invalid dimensions instead of failing every order
    return boxes


def recommend_for_lines(lines) -> Recommendation | None:
    return recommend_box(active_boxes(), items_from_lines(lines))

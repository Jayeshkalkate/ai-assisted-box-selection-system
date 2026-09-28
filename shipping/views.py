from django.shortcuts import render

# Create your views here.

import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Box, Order, Product
from .services import MAX_UNITS, InputError, recommend_for_lines

MAX_LINES = MAX_UNITS  # a line has quantity >= 1, so more lines than units can never be valid


def _serialize(rec):
    return {
        "box": {"id": rec.box.id, "name": rec.box.name, "cost": rec.box.cost,
                "inner_dimensions_cm": [rec.box.length, rec.box.width, rec.box.height],
                "max_weight_kg": rec.box.max_weight},
        "total_weight_kg": round(rec.total_weight, 3),
        "total_volume_cm3": round(rec.total_volume, 2),
        "box_volume_utilisation": round(rec.total_volume / rec.box.volume, 3),
    }


def _respond(rec):
    if rec is None:
        return JsonResponse({"error": "No available box can hold this order"}, status=422)
    return JsonResponse(_serialize(rec))


@csrf_exempt  # machine-to-machine JSON API; add token auth before exposing publicly
@require_http_methods(["POST"])
def recommend_box_view(request):
    try:
        payload = json.loads(request.body or b"{}")
    except ValueError:  # JSONDecodeError and UnicodeDecodeError are both ValueErrors
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    raw = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(raw, list) or not raw:
        return JsonResponse({"error": "'items' must be a non-empty list"}, status=400)

    if len(raw) > MAX_LINES:
        return JsonResponse({"error": f"Too many item lines (max {MAX_LINES})"}, status=400)

    merged = {}
    for row in raw:
        if not isinstance(row, dict) or not isinstance(row.get("sku"), str):
            return JsonResponse({"error": "Each item needs a string 'sku' and an integer 'quantity'"}, status=400)
        qty = row.get("quantity", 1)
        if isinstance(qty, bool) or not isinstance(qty, int) or qty < 1:
            return JsonResponse({"error": f"Invalid quantity for {row['sku']}"}, status=400)
        merged[row["sku"]] = merged.get(row["sku"], 0) + qty

    products = {p.sku: p for p in Product.objects.filter(sku__in=merged)}
    missing = sorted(set(merged) - set(products))
    if missing:
        return JsonResponse({"error": "Unknown SKU(s)", "skus": missing}, status=400)
    try:
        rec = recommend_for_lines([(products[s], q) for s, q in merged.items()])
    except InputError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    return _respond(rec)


@require_http_methods(["GET"])
def order_box_view(request, reference):
    try:
        order = Order.objects.prefetch_related("items__product").get(reference=reference)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)
    lines = [(i.product, i.quantity) for i in order.items.all()]
    if not lines:
        return JsonResponse({"error": "Order has no items"}, status=400)
    try:
        rec = recommend_for_lines(lines)
    except InputError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    return _respond(rec)



@require_http_methods(["GET"])
def home_view(request):
    """Landing page: a small UI on top of the JSON API."""
    return render(request, "shipping/index.html", {
        "products": Product.objects.order_by("sku"),
        "boxes": Box.objects.filter(is_active=True).order_by("cost", "name"),
        "orders": Order.objects.order_by("reference"),
    })


def favicon_view(request):
    return HttpResponse(status=204)

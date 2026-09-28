"""Integration tests: models + services + JSON endpoints (need Django)."""
import json

from django.test import TestCase
from django.urls import reverse

from shipping.models import Box, Order, OrderItem, Product


class ApiTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Product.objects.create(sku="BOOK", name="Book", length_cm=20, width_cm=15,
                                          height_cm=3, weight_kg=0.5)
        cls.rod = Product.objects.create(sku="ROD", name="Rod", length_cm=35, width_cm=5,
                                         height_cm=5, weight_kg=1)
        cls.heavy = Product.objects.create(sku="ANVIL", name="Anvil", length_cm=15, width_cm=15,
                                           height_cm=15, weight_kg=50)
        Box.objects.create(name="Small", inner_length_cm=25, inner_width_cm=20, inner_height_cm=10,
                           max_weight_kg=5, cost=10)
        Box.objects.create(name="Medium", inner_length_cm=40, inner_width_cm=30, inner_height_cm=30,
                           max_weight_kg=15, cost=20)
        Box.objects.create(name="Retired", inner_length_cm=100, inner_width_cm=100,
                           inner_height_cm=100, max_weight_kg=100, cost=1, is_active=False)

    def post(self, body, raw=False):
        return self.client.post(reverse("recommend-box"),
                                body if raw else json.dumps(body),
                                content_type="application/json")


class RecommendEndpointTests(ApiTestBase):
    def test_returns_cheapest_fitting_box(self):
        r = self.post({"items": [{"sku": "BOOK", "quantity": 2}]})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["box"]["name"], "Small")

    def test_inactive_box_is_never_recommended(self):
        r = self.post({"items": [{"sku": "ANVIL", "quantity": 1}]})
        self.assertEqual(r.status_code, 422)  # would fit "Retired" but it is inactive

    def test_rotation_case_via_api(self):
        r = self.post({"items": [{"sku": "ROD", "quantity": 1}]})
        self.assertEqual(r.json()["box"]["name"], "Medium")

    def test_duplicate_skus_are_merged(self):
        r = self.post({"items": [{"sku": "BOOK", "quantity": 5}, {"sku": "BOOK", "quantity": 5}]})
        self.assertEqual(r.status_code, 200)
        self.assertAlmostEqual(r.json()["total_weight_kg"], 5.0)

    def test_unknown_sku_400(self):
        r = self.post({"items": [{"sku": "NOPE", "quantity": 1}]})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["skus"], ["NOPE"])

    def test_bad_payloads_400(self):
        for body in ({}, {"items": []}, {"items": "x"}, {"items": [{"quantity": 1}]},
                     {"items": [{"sku": "BOOK", "quantity": 0}]},
                     {"items": [{"sku": "BOOK", "quantity": -3}]},
                     {"items": [{"sku": "BOOK", "quantity": "2"}]},
                     {"items": [{"sku": "BOOK", "quantity": True}]}):
            with self.subTest(body=body):
                self.assertEqual(self.post(body).status_code, 400)

    def test_invalid_json_400(self):
        self.assertEqual(self.post("{not json", raw=True).status_code, 400)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(reverse("recommend-box")).status_code, 405)

    def test_too_many_units_400(self):
        r = self.post({"items": [{"sku": "BOOK", "quantity": 100000}]})
        self.assertEqual(r.status_code, 400)


class OrderEndpointTests(ApiTestBase):
    def test_order_recommendation(self):
        order = Order.objects.create(reference="ORD-1")
        OrderItem.objects.create(order=order, product=self.book, quantity=3)
        r = self.client.get(reverse("order-box", args=["ORD-1"]))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["box"]["name"], "Small")

    def test_unknown_order_404(self):
        self.assertEqual(self.client.get(reverse("order-box", args=["X"])).status_code, 404)

    def test_empty_order_400(self):
        Order.objects.create(reference="EMPTY")
        self.assertEqual(self.client.get(reverse("order-box", args=["EMPTY"])).status_code, 400)

    def test_unfittable_order_422(self):
        order = Order.objects.create(reference="ORD-2")
        OrderItem.objects.create(order=order, product=self.heavy, quantity=1)
        self.assertEqual(self.client.get(reverse("order-box", args=["ORD-2"])).status_code, 422)

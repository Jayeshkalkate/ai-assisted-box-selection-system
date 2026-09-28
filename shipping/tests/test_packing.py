"""Unit tests for the pure packing logic (no database / Django needed)."""
import unittest

from shipping.packing import BoxSpec, Item, EPS, recommend_box, try_pack


def box(id_, name, l, w, h, max_w, cost):
    return BoxSpec(id_, name, l, w, h, max_w, cost)


def cube(size, weight=1.0, label="c"):
    return Item(size, size, size, weight, label)


def assert_valid_packing(tc, b, placements, expected_count):
    """Independent check: inside box, no two placements overlap."""
    tc.assertEqual(len(placements), expected_count)
    for p in placements:
        tc.assertGreaterEqual(p.x, -EPS)
        tc.assertGreaterEqual(p.y, -EPS)
        tc.assertGreaterEqual(p.z, -EPS)
        tc.assertLessEqual(p.x + p.l, b.length + 1e-6)
        tc.assertLessEqual(p.y + p.w, b.width + 1e-6)
        tc.assertLessEqual(p.z + p.h, b.height + 1e-6)
        # orientation must be a permutation of the item's dimensions
        tc.assertEqual(sorted((p.l, p.w, p.h)),
                       sorted((p.item.length, p.item.width, p.item.height)))
    for i, a in enumerate(placements):
        for c in placements[i + 1:]:
            separated = (a.x + a.l <= c.x + 1e-6 or c.x + c.l <= a.x + 1e-6
                         or a.y + a.w <= c.y + 1e-6 or c.y + c.w <= a.y + 1e-6
                         or a.z + a.h <= c.z + 1e-6 or c.z + c.h <= a.z + 1e-6)
            tc.assertTrue(separated, f"overlap between {a} and {c}")


class RecommendBoxTests(unittest.TestCase):
    def setUp(self):
        self.small = box(1, "S", 20, 20, 20, 5, 10)
        self.medium = box(2, "M", 40, 30, 30, 15, 20)
        self.large = box(3, "L", 60, 40, 40, 30, 35)

    def test_single_item_gets_cheapest_fitting_box(self):
        rec = recommend_box([self.large, self.medium, self.small], [cube(10, 1)])
        self.assertEqual(rec.box.name, "S")

    def test_weight_limit_skips_box(self):
        rec = recommend_box([self.small, self.medium], [cube(10, 6)])
        self.assertEqual(rec.box.name, "M")

    def test_item_too_big_for_every_box_returns_none(self):
        self.assertIsNone(recommend_box([self.small, self.medium, self.large], [cube(70)]))

    def test_all_boxes_too_light_returns_none(self):
        self.assertIsNone(recommend_box([self.small, self.medium, self.large], [cube(10, 100)]))

    def test_rotation_allows_long_item(self):
        # 35x5x5 only fits the medium box if laid along its 40 cm side
        item = Item(5, 35, 5, 1, "rod")
        rec = recommend_box([self.small, self.medium], [item])
        self.assertEqual(rec.box.name, "M")
        assert_valid_packing(self, self.medium, rec.placements, 1)

    def test_exact_fit_is_accepted(self):
        rec = recommend_box([self.small], [cube(20, 5)])
        self.assertIsNotNone(rec)
        assert_valid_packing(self, self.small, rec.placements, 1)

    def test_just_over_boundary_is_rejected(self):
        self.assertIsNone(recommend_box([self.small], [cube(20.01, 1)]))

    def test_volume_ok_but_shape_impossible(self):
        # two 15-cubes: total volume 6750 < 8000 but they cannot both fit in a 20-cube
        self.assertIsNone(recommend_box([self.small], [cube(15), cube(15)]))

    def test_multiple_items_packed_without_overlap(self):
        items = [cube(10, 0.5, f"c{i}") for i in range(8)]  # 8 cubes fill a 20-cube exactly (4 kg total)
        rec = recommend_box([self.small], items)
        self.assertIsNotNone(rec)
        assert_valid_packing(self, self.small, rec.placements, 8)

    def test_cheaper_box_wins_even_if_bigger(self):
        cheap_big = box(9, "CheapBig", 60, 40, 40, 30, 5)
        rec = recommend_box([self.small, cheap_big], [cube(10, 1)])
        self.assertEqual(rec.box.name, "CheapBig")

    def test_tie_on_cost_prefers_smaller_volume_then_id(self):
        a = box(5, "A", 30, 30, 30, 10, 10)
        b = box(4, "B", 25, 25, 25, 10, 10)
        self.assertEqual(recommend_box([a, b], [cube(10)]).box.name, "B")
        c = box(3, "C", 25, 25, 25, 10, 10)
        self.assertEqual(recommend_box([b, c], [cube(10)]).box.id, 3)

    def test_totals_reported(self):
        rec = recommend_box([self.medium], [cube(10, 2), cube(10, 3)])
        self.assertAlmostEqual(rec.total_weight, 5)
        self.assertAlmostEqual(rec.total_volume, 2000)

    def test_empty_items_raises(self):
        with self.assertRaises(ValueError):
            recommend_box([self.small], [])

    def test_no_boxes_returns_none(self):
        self.assertIsNone(recommend_box([], [cube(5)]))

    def test_input_order_does_not_change_result(self):
        items = [cube(10, 1), Item(5, 20, 5, 1), cube(8, 1)]
        r1 = recommend_box([self.small, self.medium], items)
        r2 = recommend_box([self.medium, self.small], list(reversed(items)))
        self.assertEqual(r1.box, r2.box)


class ValidationTests(unittest.TestCase):
    def test_zero_dimension_item_rejected(self):
        with self.assertRaises(ValueError):
            Item(0, 5, 5, 1)

    def test_negative_weight_rejected(self):
        with self.assertRaises(ValueError):
            Item(5, 5, 5, -1)

    def test_bad_box_rejected(self):
        with self.assertRaises(ValueError):
            BoxSpec(1, "bad", 10, -1, 10, 5, 1)
        with self.assertRaises(ValueError):
            BoxSpec(1, "bad", 10, 10, 10, 5, -1)


class TryPackTests(unittest.TestCase):
    def test_try_pack_returns_none_when_full(self):
        b = box(1, "S", 10, 10, 10, 50, 1)
        self.assertIsNone(try_pack(b, [cube(10), cube(1)]))


if __name__ == "__main__":
    unittest.main()

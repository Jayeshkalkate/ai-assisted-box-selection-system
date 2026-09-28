"""Pure-Python box selection logic (no Django imports, so it is easy to unit test).

Approach
--------
1. Cheap necessary checks (reject early):
   - total item weight <= box max weight
   - total item volume  <= box volume
   - every single item fits the box in at least one of its 6 orientations
2. Packing heuristic ("extreme points"): place items largest-first; try
   candidate corner points, trying every orientation; accept the first
   placement that stays inside the box and overlaps nothing.
3. Among boxes that pass, pick the cheapest (tie-break: smaller volume, then id).

Limitations (be honest about them)
----------------------------------
3D bin packing is NP-hard. The heuristic never accepts an impossible packing
(placements are verified not to overlap or leave the box), but it can reject a
packing that exists. In that case a larger box is recommended, which is safe
for the warehouse but may cost more. Items are treated as rigid boxes; no
stacking limits, fragility, or padding are modelled. All units: cm and kg.
"""
from dataclasses import dataclass
from itertools import permutations
from typing import List, Optional, Sequence

EPS = 1e-9


@dataclass(frozen=True)
class Item:
    length: float
    width: float
    height: float
    weight: float
    label: str = ""

    def __post_init__(self):
        for name in ("length", "width", "height"):
            if not getattr(self, name) > 0:
                raise ValueError(f"Item '{self.label}': {name} must be > 0")
        if self.weight < 0:
            raise ValueError(f"Item '{self.label}': weight must be >= 0")

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height


@dataclass(frozen=True)
class BoxSpec:
    id: int
    name: str
    length: float
    width: float
    height: float
    max_weight: float
    cost: float

    def __post_init__(self):
        for name in ("length", "width", "height", "max_weight"):
            if not getattr(self, name) > 0:
                raise ValueError(f"Box '{self.name}': {name} must be > 0")
        if self.cost < 0:
            raise ValueError(f"Box '{self.name}': cost must be >= 0")

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height


@dataclass(frozen=True)
class Placement:
    item: Item
    x: float
    y: float
    z: float
    l: float
    w: float
    h: float


@dataclass(frozen=True)
class Recommendation:
    box: BoxSpec
    placements: List[Placement]
    total_weight: float
    total_volume: float


def _fits_alone(box: BoxSpec, item: Item) -> bool:
    """An item fits alone if its sorted dims fit inside the box's sorted dims."""
    a = sorted((item.length, item.width, item.height))
    b = sorted((box.length, box.width, box.height))
    return all(x <= y + EPS for x, y in zip(a, b))


def _overlaps(p: Placement, x, y, z, l, w, h) -> bool:
    return (
        x < p.x + p.l - EPS and p.x < x + l - EPS
        and y < p.y + p.w - EPS and p.y < y + w - EPS
        and z < p.z + p.h - EPS and p.z < z + h - EPS
    )


def try_pack(box: BoxSpec, items: Sequence[Item]) -> Optional[List[Placement]]:
    """Return a list of placements if the heuristic finds a packing, else None."""
    ordered = sorted(items, key=lambda i: (-i.volume, -max(i.length, i.width, i.height)))
    placed: List[Placement] = []
    points = [(0.0, 0.0, 0.0)]

    for item in ordered:
        orientations = sorted(set(permutations((item.length, item.width, item.height))))
        done = False
        for pt in sorted(points, key=lambda p: (p[2], p[1], p[0])):
            x, y, z = pt
            for l, w, h in orientations:
                if (x + l > box.length + EPS or y + w > box.width + EPS
                        or z + h > box.height + EPS):
                    continue
                if any(_overlaps(p, x, y, z, l, w, h) for p in placed):
                    continue
                placed.append(Placement(item, x, y, z, l, w, h))
                points.remove(pt)
                points.extend([(x + l, y, z), (x, y + w, z), (x, y, z + h)])
                done = True
                break
            if done:
                break
        if not done:
            return None
    return placed


def recommend_box(boxes: Sequence[BoxSpec], items: Sequence[Item]) -> Optional[Recommendation]:
    """Cheapest box that can hold all items, or None if no box works."""
    if not items:
        raise ValueError("Order has no items")
    total_weight = sum(i.weight for i in items)
    total_volume = sum(i.volume for i in items)

    for box in sorted(boxes, key=lambda b: (b.cost, b.volume, b.id)):
        if total_weight > box.max_weight + EPS:
            continue
        if total_volume > box.volume + EPS:
            continue
        if not all(_fits_alone(box, i) for i in items):
            continue
        placements = try_pack(box, items)
        if placements is not None:
            return Recommendation(box, placements, total_weight, total_volume)
    return None

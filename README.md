# AI-Assisted Box Selection System

A small Django service that recommends the most suitable shipping box for an ecommerce order.

The selection engine is intentionally kept independent from Django so the core packing logic can be tested without a database. The API layer converts database records into packing inputs and returns a compact JSON recommendation.

## Problem

For each order, the warehouse needs a box that:

- can physically contain every product;
- can support the total product weight;
- respects product rotation;
- does not overlap products while packing;
- is selected by shipping cost, with deterministic tie-breaks.

The system assumes rectangular, rigid products and boxes. Units are centimetres and kilograms.

## Project structure

```text
box-selector/
├── box_selector/               # Django project configuration
├── shipping/
│   ├── migrations/             # Database schema
│   ├── tests/
│   │   ├── test_packing.py     # Pure algorithm tests
│   │   └── test_api.py         # Django API tests
│   ├── admin.py
│   ├── models.py               # Product, Box, Order, OrderItem
│   ├── packing.py              # Pure-Python packing engine
│   ├── services.py             # DB → packing-engine adapter
│   ├── urls.py
│   └── views.py                # JSON API
├── chat_transcript/
├── .github/workflows/ci.yml
├── AI_USAGE.md
├── LEARNINGS.md
├── TEST_OUTPUT.md
├── manage.py
└── requirements.txt
```

## Selection approach

The algorithm does not rely only on volume. For each active box it performs:

1. **Weight check** — total order weight must be within the box capacity.
2. **Volume check** — total item volume must be within the box volume.
3. **Individual fit check** — every item must fit in at least one of its six axis-aligned orientations.
4. **Packing check** — items are ordered largest-first and placed using an extreme-point style heuristic.
5. **Cost selection** — among boxes successfully packed, the lowest cost wins. Ties use smaller box volume and then database ID.

The packing routine records `(x, y, z)` coordinates and the chosen orientation for every item. A candidate placement is accepted only when it remains inside the box and does not overlap an existing placement.

### Important limitation

3D bin packing is NP-hard. This implementation is a deterministic heuristic, not an exact optimizer. It will never accept a placement that overlaps another item, but a valid packing may occasionally be missed. In that situation the service can fall back to a larger box.

The implementation also does not model padding, fragile-item rules, stacking limits, weight distribution, or "this side up" constraints.

## API

### Recommend a box for an order payload

```http
POST /api/recommend-box/
Content-Type: application/json
```

Example:

```json
{
  "items": [
    {"sku": "BOOK", "quantity": 2},
    {"sku": "ROD", "quantity": 1}
  ]
}
```

Successful response:

```json
{
  "box": {
    "id": 2,
    "name": "Medium",
    "cost": 20.0,
    "inner_dimensions_cm": [40.0, 30.0, 30.0],
    "max_weight_kg": 15.0
  },
  "total_weight_kg": 2.0,
  "total_volume_cm3": 2950.0,
  "box_volume_utilisation": 0.082
}
```

Other responses:

| Status | Meaning |
|---|---|
| 200 | A suitable active box was found |
| 400 | Invalid JSON, invalid quantity, empty item list, or unknown SKU |
| 404 | Requested order reference does not exist |
| 405 | HTTP method is not supported |
| 422 | No active box can hold the complete order |

### Recommend a box for an existing order

```http
GET /api/orders/ORD-1001/box/
```

## Local setup

Python 3.12 is recommended.

### 1. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create and apply migrations

```bash
python manage.py makemigrations shipping
python manage.py migrate
```

Commit the generated `shipping/migrations/0001_initial.py`.

### 4. Create an admin user

```bash
python manage.py createsuperuser
```

### 5. Start Django

```bash
python manage.py runserver
```

Open the Django admin at `http://127.0.0.1:8000/admin/`.

Add products, active boxes and orders through the admin interface.

## PostgreSQL

SQLite is the default for a quick local setup. To use PostgreSQL, configure:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
```

Install the driver first: `pip install "psycopg[binary]"`. It is only needed when PostgreSQL is selected.

## Testing

Run the complete Django test suite:

```bash
python manage.py test -v 2
```

The suite covers:

- exact boundary fits;
- rotation;
- weight and volume rejection;
- impossible geometry;
- multiple-item packing;
- cost and tie-break rules;
- input validation;
- inactive boxes;
- duplicate SKU merging;
- unknown SKUs;
- empty and unknown orders;
- HTTP method handling.

CI runs `manage.py check` and the Django test suite on every push and pull request.

## Security notes

The assignment API is intentionally simple and has no authentication layer. The recommendation endpoint is CSRF-exempt because it is designed as a machine-to-machine JSON endpoint.

Before exposing it publicly, add API authentication (for example, token-based authentication), rate limiting, structured request logging, and production Django security settings.

## Environment variables

Copy `.env.example` to `.env` for reference. Django does not read `.env` by itself, so export the values in your shell (for example `DJANGO_SECRET_KEY`) before running the server.

## Reviewer files

`AI_USAGE.md`, `LEARNINGS.md`, `TEST_OUTPUT.md`, `chat_transcript/`.

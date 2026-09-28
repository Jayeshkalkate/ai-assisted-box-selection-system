
/

I reviewed the assignment itself and cross-checked the testing expectations against current Django/DRF documentation. The important point is that this is **not primarily a CRUD Django assignment**. It is a small backend engineering problem where the evaluator is likely looking at your **reasoning, d

pasted

 generate the project files from the given instructions
Building API endpoints and serializers for order recommendations.
I'll build the project, run the tests for real, and package it.

Ran a command
Claude’s response was interrupted.
As per the given instructions, give me a zip file of the project. give me fast before your limit is ended
Ran a command, shared files
Your project zip is ready below. All 22 tests pass.

What's inside

App code: a Django and DRF app with Product, Box, Order and OrderItem models, migrations included.
Selection logic: it lives in boxes/services.py, separate from the API. A box is valid if every unit fits (rotation allowed), the total weight is within the limit, and the total volume is at most 85% of the box volume. The cheapest valid box wins, with ties broken by smallest volume and then lowest id.
API:
POST /api/orders/
GET /api/orders/<id>/recommendation/, which returns 422 with per-box rejection reasons when nothing fits
CRUD endpoints for /api/products/ and /api/boxes/
Tests: unit, model and API tests, plus a GitHub Actions workflow (.github/workflows/tests.yml).
Docs: README.md with assumptions, limitations and the API, and TEST_OUTPUT.md with the real test run.
Things you must do yourself. The assignment forbids AI-generated versions of these, so I left them as blank templates:

chat-transcript/: export your actual conversation and put it here.
LEARNINGS.md: write it in your own words.
AI_USAGE.md: fill it with what really happened, including the prompts you gave, what you accepted or rejected, and any mistakes.
Before you submit

Run pip install -r requirements.txt, then python manage.py migrate and python manage.py test.
Replace TEST_OUTPUT.md with your own run, since a real run on your machine is stronger evidence.
The volume rule is a heuristic, not true 3D packing. The README says so, and you should be ready to explain it.

Django box selector
ZIP 


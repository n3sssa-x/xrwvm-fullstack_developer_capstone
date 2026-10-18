# Quick README for the mock backend

This mock backend is included to help you test the frontend and Django layers
locally without requiring the real backend deployment.

To run the mock backend:

1) Install Flask (if not already installed):

   python3 -m pip install --user flask

2) Start the mock backend in a terminal:

   python3 server/mock_backend.py

It listens on http://localhost:3030 and provides the endpoints the Django
app expects:
- GET  /fetchDealers
- GET  /fetchDealers/<state>
- GET  /fetchDealer/<id>
- GET  /fetchReviews/dealer/<id>
- POST /insert_review

When testing locally, set server/djangoapp/.env to:

backend_url = http://localhost:3030

Then restart the Django server and rebuild frontend if necessary.

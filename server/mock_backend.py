"""Mock backend for local testing of the Capstone frontend + Django layers.

This lightweight Flask application implements the minimal endpoints
that the Django app expects from the backend API so you can test
end-to-end locally without the real backend deployment.

Endpoints implemented:
- GET  /fetchDealers
- GET  /fetchDealers/<state>
- GET  /fetchDealer/<dealer_id>
- GET  /fetchReviews/dealer/<dealer_id>
- POST /insert_review

Run:
  python3 server/mock_backend.py

(The app listens on 0.0.0.0:3030)

NOTE: This is for local/testing only. It returns static sample data.
"""
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Sample data
DEALERS = [
    {"id": 1, "full_name": "First Dealer", "city": "CityA", "address": "123 A St", "zip": "11111", "state": "CA"},
    {"id": 2, "full_name": "Second Dealer", "city": "CityB", "address": "456 B Ave", "zip": "22222", "state": "NY"},
    {"id": 3, "full_name": "Third Dealer", "city": "CityC", "address": "789 C Rd", "zip": "33333", "state": "TX"}
]

REVIEWS = {
    1: [
        {"review_id": 101, "review": "Great service", "name": "Alice", "car_make": "Honda", "car_model": "Civic", "car_year": 2019, "sentiment": "positive"}
    ],
    2: [
        {"review_id": 102, "review": "Okay experience", "name": "Bob", "car_make": "Toyota", "car_model": "Corolla", "car_year": 2018, "sentiment": "neutral"}
    ]
}

@app.route('/fetchDealers', methods=['GET'])
def fetch_dealers():
    return jsonify(DEALERS)

@app.route('/fetchDealers/<state>', methods=['GET'])
def fetch_dealers_by_state(state):
    filtered = [d for d in DEALERS if d.get('state') == state]
    return jsonify(filtered)

@app.route('/fetchDealer/<int:dealer_id>', methods=['GET'])
def fetch_dealer(dealer_id):
    for d in DEALERS:
        if d['id'] == dealer_id:
            return jsonify(d)
    return jsonify({}), 404

@app.route('/fetchReviews/dealer/<int:dealer_id>', methods=['GET'])
def fetch_reviews(dealer_id):
    return jsonify(REVIEWS.get(dealer_id, []))

@app.route('/insert_review', methods=['POST'])
def insert_review():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "invalid JSON"}), 400

    # very small validation
    if not data or 'dealership' not in data or 'review' not in data:
        return jsonify({"status": "error", "message": "missing fields"}), 400

    dealer_id = int(data.get('dealership'))
    new_id = max([r.get('review_id', 100) for revs in REVIEWS.values() for r in revs] + [100]) + 1
    review_item = {
        "review_id": new_id,
        "review": data.get('review'),
        "name": data.get('name', 'Anonymous'),
        "car_make": data.get('car_make'),
        "car_model": data.get('car_model'),
        "car_year": data.get('car_year'),
        "sentiment": "neutral",
        "purchase_date": data.get('purchase_date')
    }
    REVIEWS.setdefault(dealer_id, []).append(review_item)

    # return simple success response similar to what the real backend might return
    return jsonify({"status": "ok", "review_id": new_id}), 201

if __name__ == '__main__':
    # Run the mock backend on port 3030
    app.run(host='0.0.0.0', port=3030)

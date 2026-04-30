"""Simulated internal billing microservice on port 5001.

Represents a neighbouring service reachable from the application server
(loopback / internal network) but not from the public internet.
Run alongside app.py:  python internal_service.py
"""

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

BILLING_RECORDS = [
    {"order_id": "ORD-0001", "username": "alice",   "event": "metallica",      "amount_eur": 145, "card_last4": "4242"},
    {"order_id": "ORD-0002", "username": "bob",     "event": "taylor-swift",   "amount_eur": 320, "card_last4": "1337"},
    {"order_id": "ORD-0003", "username": "charlie", "event": "coldplay",       "amount_eur": 95,  "card_last4": "9999"},
    {"order_id": "ORD-0004", "username": "diana",   "event": "the-weeknd",     "amount_eur": 180, "card_last4": "0000"},
    {"order_id": "ORD-0005", "username": "root",    "event": "adele",          "amount_eur": 350, "card_last4": "1111"},
]

DB_CONFIG = {
    "host": "10.0.1.10",
    "port": 5432,
    "name": "ticketoracle_billing",
    "user": "billing_svc",
    "password": "Str0ngP@ssw0rd!",
}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "billing", "version": "1.4.2"})


@app.route("/billing/orders")
def billing_orders():
    return jsonify(BILLING_RECORDS)


@app.route("/billing/orders/<username>")
def billing_orders_by_user(username):
    records = [r for r in BILLING_RECORDS if r["username"] == username]
    if not records:
        return jsonify({"error": "No orders found"}), 404
    return jsonify(records)


@app.route("/billing/config")
def billing_config():
    return jsonify(DB_CONFIG)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)

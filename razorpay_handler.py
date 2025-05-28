import hmac
import hashlib
import os
from flask import jsonify

RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

def handle_razorpay_webhook(request):
    payload = request.data
    signature = request.headers.get('X-Razorpay-Signature')

    if not verify_signature(payload, signature):
        return jsonify({"status": "error", "message": "Invalid signature"}), 400

    data = request.get_json()
    # Process based on event type
    if data.get("event") == "payment.captured":
        email = data['payload']['payment']['entity']['email']
        amount = int(data['payload']['payment']['entity']['amount']) / 100
        tier = "premium" if amount >= 499 else "pro"
        with open("user_tiers.txt", "a") as f:
            f.write(f"{email},{tier}\n")
        return jsonify({"status": "success", "message": "Tier updated"}), 200

    return jsonify({"status": "ignored"}), 200

def verify_signature(payload, signature):
    generated = hmac.new(RAZORPAY_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(generated, signature)

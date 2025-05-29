from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)

# Load secret from environment variable
RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "mycaiohooksecret")

@app.route('/')
def health_check():
    return "CAIO Webhook Live", 200

@app.route('/webhook', methods=['POST'])
def razorpay_webhook():
    try:
        payload = request.get_data()
        signature = request.headers.get('X-Razorpay-Signature')

        # Verify webhook signature
        expected_signature = hmac.new(
            key=RAZORPAY_WEBHOOK_SECRET.encode('utf-8'),
            msg=payload,
            digestmod=hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return jsonify({'error': 'Invalid signature'}), 400

        # Parse and log the payload
        data = request.get_json()
        event = data.get('event')
        payment_info = data.get('payload', {}).get('payment', {}).get('entity', {})

        print(f"[CAIO LOG] Event: {event}")
        print(f"[CAIO LOG] Payment Info: {payment_info}")

        # Optional: Store in CRM or database
        # save_to_crm(payment_info)

        # Optional: Trigger alert email (setup SendGrid or SMTP later)
        # send_email_alert("New Razorpay payment", str(payment_info))

        return jsonify({'status': 'Webhook received'}), 200

    except Exception as e:
        print(f"[CAIO ERROR] {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)

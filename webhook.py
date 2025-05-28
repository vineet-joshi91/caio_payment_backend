from flask import Flask, request, jsonify
from razorpay_handler import handle_razorpay_webhook
# from paypal_handler import handle_paypal_webhook  # Future expansion
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "CAIO Payment Webhook Server is Running"

@app.route('/razorpay-webhook', methods=['POST'])
def razorpay_webhook():
    return handle_razorpay_webhook(request)

# @app.route('/paypal-webhook', methods=['POST'])  # Future expansion
# def paypal_webhook():
#     return handle_paypal_webhook(request)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

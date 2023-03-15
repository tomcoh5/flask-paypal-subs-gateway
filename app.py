from flask import Flask, render_template,jsonify, request,redirect,url_for,flash
import paypalrestsdk
from paypalrestsdk import BillingPlan
from datetime import datetime

app = Flask(__name__)

paypalrestsdk.configure({
    "mode":"sandbox",
    "client_id":"AVtwtiiF7mtOFBgTVMi20LBN5g7paKgC8HuJCbDApHWJuK6-VfAe6lIo9v4MSWYQdIsgwuchQzAoAE4L",
    "client_secret":"EBiH0rZ-6x_MwkLeWrwKnQROKXBeh3ixqXy2aL7Qf9TUjp5sMexLgF1N77AAtcBy3k8CumPEF-Vuxcik"
})

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/payment', methods=['POST'])
# def payment():

#     payment = paypalrestsdk.Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal"},
#         "redirect_urls": {
#             "return_url": "http://localhost:5000/payment/execute",
#             "cancel_url": "http://localhost:5000/"},
#         "transactions": [{
#             "item_list": {
#                 "items": [{
#                     "name": "testitem",
#                     "sku": "12345",
#                     "price": "500.00",
#                     "currency": "USD",
#                     "quantity": 1}]},
#             "amount": {-
#                 "total": "500.00",
#                 "currency": "USD"},
#             "description": "This is the payment transaction description."}]})

#     if payment.create():
#         print('Payment success!')
#     else:
#         print(payment.error)

#     return jsonify({'paymentID' : payment.id})


@app.route('/execute', methods=['POST'])
def execute():

    payment = paypalrestsdk.subs.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success !')
        success = True
    else:
        print(payment.error)
    return jsonify({'success' : success})

@app.route('/subscribe', methods=['POST'])
def subscribe():
    billing_plan = BillingPlan({
    "name": "Fast Speed Plan",
    "description": "Create Plan for Regular",
    "merchant_preferences": {
        "auto_bill_amount": "yes",
        "cancel_url": "http://localhost:5000/subscribe",
        "initial_fail_amount_action": "continue",
        "max_fail_attempts": "1",
        "return_url": "http://localhost:5000/",
        "setup_fee": {
            "currency": "USD",
            "value": "25"
        }
    },
    "payment_definitions": [
        {
            "amount": {
                "currency": "USD",
                "value": "100"
            },
            "charge_models": [
                {
                    "amount": {
                        "currency": "USD",
                        "value": "10.60"
                    },
                    "type": "SHIPPING"
                },
                {
                    "amount": {
                        "currency": "USD",
                        "value": "20"
                    },
                    "type": "TAX"
                }
            ],
            "cycles": "0",
            "frequency": "MONTH",
            "frequency_interval": "1",
            "name": "Regular 1",
            "type": "REGULAR"
        }
    ],
    "type": "INFINITE"
})

    response = billing_plan.create()
    print(response)


    # Retrieve subscription ID from the response
    subscription_id = response.id

    # Return subscription ID as JSON response
    print(subscription_id)
    return {'subscription_id': subscription_id}
    
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template,jsonify, request
import paypalrestsdk

app = Flask(__name__)


paypalrestsdk.configure({
    "mode":"sandbox",
    "client_id":"AVtwtiiF7mtOFBgTVMi20LBN5g7paKgC8HuJCbDApHWJuK6-VfAe6lIo9v4MSWYQdIsgwuchQzAoAE4L",
    "client_secret":"EBiH0rZ-6x_MwkLeWrwKnQROKXBeh3ixqXy2aL7Qf9TUjp5sMexLgF1N77AAtcBy3k8CumPEF-Vuxcik"
})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:5000/payment/execute",
            "cancel_url": "http://localhost:5000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "500.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "500.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})


@app.route('/execute', methods=['POST'])
def execute():

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute success !')
        success = True
    else:
        print(payment.error)
    return jsonify({'success' : success})


if __name__ == '__main__':
    app.run(debug=True)
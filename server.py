from flask import Flask, Blueprint, request
# from Services.Data import Service
import json
import os
app = Flask(__name__)

data_router = Blueprint('data_router', __name__)

@app.route('/signup', methods = ["GET"])
def create_subscription():
    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password)
    try:
    #     obj = Service()
    #     customer_data = stripe.Customer.list(email=email).data   
    #     customer, default_payment_method = obj.customer(customer_data, email, payment_method_id)
    #     subs_data = {
    #         "customer": customer,
    #         "default_payment_method": default_payment_method
    #     }
    #     subscription = obj.create_subscription(subs_data)
    #     print("subscription ==============>", subscription)
        data = {"hello": "hello"}
        return {"status" : "Success", "data": data}, 200
    except Exception as e:
        return {"status" : "Failure", "message": f"{e}"}, 500

if __name__ == "__main__":
    app.run("0.0.0.0", 80, debug = True)
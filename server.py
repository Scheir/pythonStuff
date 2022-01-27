# -----------------------------------------------------------
# Order handler API. Supports creation and retrieving of
# customers aswell as creation, update and retrieving of 
# orders issues by customers. 
# 
# The endpoints used are /customer for customer requests,
# endpoints for order requests are /order.
#
# A mongoDB is used as database and the only prerequisites
# is a mongodb collection of available items to put in the 
# order cart.
#
# Customers and orders collections will be created
# automatically if empty.
#
# Examples of request bodies can be found in the README.md
# file of this repo, aswell as restrictions are implicitly 
# read from json schemas in request_schemas.
# 
# Run the API by python3 server.py
#
# 2021 Andre Scheir Johansson
# email: scheir5@hotmail.se
# -----------------------------------------------------------


import json
from request_handler import Request_handler as rh
from flask import Flask, request, jsonify, Response

def create_response(body, code) -> Response:
    return Response(json.dumps(body), status=code, mimetype='application/json')

app = Flask(__name__)


@app.route('/customer', methods=['GET'])
def get_customer():
    """
    Customer get request.
    Retrieves a customer object from database by customer name.
    """
    data = json.loads(request.data)
    ret,code = rh.handle_get_customer(data)
    print(ret)
    return create_response(ret,code) 

@app.route('/customer', methods=['POST'])
def create_customer():
    """
    Customer POST request.
    Creates a customer entry in database.
    """
    data = json.loads(request.data)
    ret,code = rh.handle_create_customer(data)
    return create_response(ret,code)


@app.route('/order', methods=['GET'])
def get_order():
    """
    Order get request.
    Retrievs an order by id from database.
    """
    data = json.loads(request.data)
    ret,code = rh.handle_get_order(data)
    return create_response(ret,code)

@app.route('/order', methods=['POST'])
def create_order():
    """
    Order POST request.
    Creates an order by customer and a cart
    containing items and quantities.
    """
    data = json.loads(request.data)
    ret,code = rh.handle_create_order(data)
    return create_response(ret,code)

@app.route('/order', methods=['PUT'])
def update_order():
    """
    Order PUT request.
    Updates an order by order id and a cart
    containing items and quantities.
    """
    data = json.loads(request.data)
    ret,code = rh.handle_update_order(data)
    return create_response(ret,code)

# 
app.run()
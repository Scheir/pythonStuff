import json
from request_handler import RequestHandler as rh
from flask import Flask, request, jsonify, Response

def create_response(body, code) -> Response:
    return Response(json.dumps(body), status=code, mimetype='application/json')

app = Flask(__name__)


@app.route('/customer', methods=['GET'])
def get_customer():
    data = json.loads(request.data)
    ret,code = rh.handle_get_customer(data)
    print(ret)
    return create_response(ret,code) 

@app.route('/customer', methods=['PUT'])
def create_customer():
    data = json.loads(request.data)
    ret,code = rh.handle_create_customer(data)
    return create_response(ret,code)


@app.route('/order', methods=['GET'])
def get_order():
    data = json.loads(request.data)
    ret,code = rh.handle_get_order(data)
    return create_response(ret,code)

@app.route('/order', methods=['PUT'])
def create_order():
    data = json.loads(request.data)
    ret,code = rh.handle_create_order(data)
    return create_response(ret,code)


app.run()
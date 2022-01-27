import jsonschema
from database import db
from jsonschema import validate
from collections import ChainMap
from customer import Customer
from order import Order

customer_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type":"string",
            "pattern": "^[a-zA-Z0-9 ]+$"
        },
        "type": {
            "type":"string",
            "pattern": "^(Big Company)|(Small Company)|(Private)$"
        }
    },
    "additionalProperties": False,
    "required": [
    "name",
    "type"
  ]
}
order_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "cart": {
            "type": "array",
            "items":{
                "type":"object",
            },
            "minItems":1
        }
    },
    "additionalProperties": False,
    "required": [
        "name",
        "cart"
    ]
}

order_id_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        }
    },
    "additionalProperties": False,
    "required": [
        "id"
    ]
}

class RequestHandler:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def __validate_data(data, schema) -> bool:
        try:
            validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

    @staticmethod
    def handle_get_customer(data) -> tuple:
        # Check if data is valid
        db_inst = db.get_instance()
        customer = db_inst.get_customer(data.get("name"))
        if not customer:
            return ("Customer not found", 400)
        #TODO:
        print("Get", customer)
        return customer, 200
            
    @staticmethod
    def handle_create_customer(data) -> tuple:
        # Check if data is valid
        if not RequestHandler.__validate_data(data, customer_schema):
            return "Invalid json content", 400
        
        new_cust = Customer(data)
        db_inst = db.get_instance()
        if db_inst.create_customer(new_cust):
            return "OK", 200
        else:
            return "Failed to create customer", 400
    
    @staticmethod
    def handle_create_order(data) -> tuple:
        # Check if data is valid.
        # We only check if structure is ok here
        if not RequestHandler.__validate_data(data, order_schema):
            return ("Invalid json content order", 400)
        
        # item:quantity dict
        cart = dict(ChainMap(*data.get("cart")))
        db_inst = db.get_instance()
        customer = db_inst.get_customer(data.get("name", None))
        if not customer:
            return "Could not find customer", 400

        #TODO: Check that all cart_items are in the db
        #if not db_inst.find_items(cart_items):
        # 
        #
        order = Order(customer, cart)
        if not db_inst.create_order(order):
            return ("Failed to create order", 400)
        return (order,200)

    @staticmethod
    def handle_get_order(data) -> tuple:
        # Check Json
        if not RequestHandler.__validate_data(data, order_id_schema):
            return "Invalid json content", 400

        #Get the order by order ID
        db_inst = db.get_instance()
        order_id = data.get("id")
        order = db_inst.get_order(order_id)
        if not order:
            return {"Failed":f"Did not find order with id: {order_id}"}, 400
        
        return order, 200

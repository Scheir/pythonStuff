# -----------------------------------------------------------
# The class Request_handler handles all requests routed via
# the API server.py. 
# 
# The class verifies that the requests body is good.
# 
# Creates objects (customers, orders) via their classes
# respectively during post/put requests.
# 
# Uses a DB instance to either create/update or query
# the database depending on type of request.
#
# Finally returns back to the server status code and response 
# body.
#
# 2021 Andre Scheir Johansson
# email: scheir5@hotmail.se
# -----------------------------------------------------------

import jsonschema
from database import db
from jsonschema import validate
from collections import ChainMap
from customer import Customer
from order import Order
from request_schemas import *

class Request_handler:
    """
    This class has static methods to handle all the differnt
    requests picked up by the server.
    It doesnt need or have any own data
    """
    def __init__(self) -> None:
        """
        Not used, only static methods
        """
        pass
    
    @staticmethod
    def __validate_data(data, schema) -> bool:
        """
        Validate if the requests data matches a json schema

        :param data: request data to verify
        :param schema: Json schema to compare data with
        """
        try:
            validate(instance=data, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

    @staticmethod
    def handle_get_customer(data) -> tuple:
        """
        Handle get customer request.
        Query db by customer name
        
        :param data Request data
        """
        # Check if data is valid
        customer_name_schema
        if not Request_handler.__validate_data(data, customer_name_schema):
            return "Invalid json content", 400

        db_inst = db.get_instance()
        customer = db_inst.get_customer(data.get("name"))
        if not customer:
            return ("Customer not found", 404)
        return customer, 200
            
    @staticmethod
    def handle_create_customer(data) -> tuple:
        """
        Handle create customer (post) request.
        Create a Customer object from request data
        and store in the DB
        
        :param data Request data
        """
        # Check if data is valid
        if not Request_handler.__validate_data(data, customer_schema):
            return "Invalid json content", 400
        
        new_cust = Customer(data)
        db_inst = db.get_instance()
        created_customer = db_inst.create_customer(new_cust)
        if not created_customer:
            return f'Customer: {new_cust.name} allready exists', 400
        return created_customer, 201
    
    @staticmethod
    def handle_create_order(data) -> tuple:
        """
        Handle create order (post) request.
        Create an Order object from requests data
        and store it in the db.
        
        :param data Request data
        """
        # Check if data is valid.
        # We only check if structure is ok here
        if not Request_handler.__validate_data(data, order_schema):
            return ("Invalid json content order", 400)
        
        # Transform the cart list into a dict.
        cart = dict(ChainMap(*data.get("cart")))
        db_inst = db.get_instance()
        customer = db_inst.get_customer(data.get("name", None))
        if not customer:
            return "Could not find customer", 404

        order = Order(customer, cart)
        
        # If order has failed items, tell user which items 
        # that wasnt found in the DB.
        if order.failed_items:
            return ({"Failed items":order.failed_items}, 404)
        created_order = db_inst.create_order(order)
        if not created_order:
            return ("Failed to create order", 400)
        return (created_order,201)

    @staticmethod
    def handle_get_order(data) -> tuple:
        """
        Handle get order request.
        Query the DB by requests data which contains 
        order id.

        :param data Request data
        """
        # Check Json
        if not Request_handler.__validate_data(data, order_id_schema):
            return "Invalid json content", 400

        #Get the order by order ID
        db_inst = db.get_instance()
        order_id = data.get("id")
        order = db_inst.get_order(order_id)
        if not order:
            return {"Failed":f"Did not find order with id: {order_id}"}, 404
        
        return order, 200

    @staticmethod
    def handle_update_order(data) -> tuple:
        """
        Handle update order (put) request.
        Query an existing order from the DB by 
        order id.

        Create a new Order object and update the db 
        with the new order
        
        :param data Request data
        """
        # Check Json
        if not Request_handler.__validate_data(data, order_update_schema):
            return "Invalid json content", 400
        
        #Check if order exists
        db_inst = db.get_instance()
        order_id = data.get("id")
        order = db_inst.get_order(order_id)
        if not order:
            return {"Failed":f"Did not find order with id: {order_id}"}, 404

        # Get customer
        #customer = db_inst.get_customer(data.get("name", None))
        customer = db_inst.get_customer(order.get("customer", None))
        if not customer:
            return "Could not find customer", 400
        cart = dict(ChainMap(*data.get("cart")))

        # Create a new order object
        order = Order(customer, cart)

        # If order has failed items, tell user which items 
        # that wasnt found in the DB.
        if order.failed_items:
            return ({"Failed items":order.failed_items}, 404)
        created_order = db_inst.update_order(order_id, order)
        if not created_order:
            return ("Failed to create order", 400)
        return (created_order,201)

# -----------------------------------------------------------
# The db class contains all functionality towards the mongoDB.
# It is a singleton and the instance can be obtained from 
# db.get_instance() method.
#
#
# 2021 Andre Scheir Johansson
# email: scheir5@hotmail.se
# -----------------------------------------------------------

from singleton import Singleton
import json
from customer import Customer
import pymongo
from bson import ObjectId


DB_NAME = "test2"

@Singleton
class db:
    """
    Singleton which interacts with mongoDB.

    Attributes
    ----------
    client: mongDB client
    db: mongoDB database taken from client
    
    """
    def __init__(self) -> None:
        """
        Constructor
        """
        #Open connection once
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[DB_NAME]
    
    def __str__(self):
       return f'DB instance {self.client}, {self.db}'
    
    def create_customer(self, new_cust) -> dict:
        """
        Store a new customer to the db if customer
        doesnt allready exist.

        :param new_cust Customer object
        """
        column = self.db["customers"]
        # Need to handle a case when customer allready exists
        # If we find a query skip inserting and tell user
        query_res = column.find_one({"name":new_cust.name})
        if query_res:
            return False 
        
        #Insert customer, query it and return to user
        column.insert_one(new_cust.dictify())
        return self.get_customer(new_cust.name)
    
    def get_customer(self, customer) -> dict:
        """
        Query a customer from the database

        :param customer Customer object to query
        """
        column = self.db["customers"]
        query_res = column.find_one({"name":customer},{"_id":0})
        return query_res

    def create_order(self, order) -> dict:
        """
        Store/create a new order to the database

        :param order Order to create
        """
        column = self.db["orders"]
        created_order_id = column.insert_one(order.dictify()).inserted_id

        # Order is created, get the db entry and return it
        return self.get_order(created_order_id)
        
    def get_order(self, order_id) -> dict:
        """
        Query an order from the database

        :param order_id id of order to query
        """
        
        column = self.db["orders"]     
        # Check if Order id has wrong format
        try:
            query_res = column.find_one({"_id":ObjectId(order_id)})
        except:
            return None

        # Order id format ok, but order doesnt exist
        if not query_res:
            return None

        # Nasty bug where the id field in the mongoDB is nasty.
        # Work around by deleting the field and inserting it again as a string.
        query_res["id"] = str(query_res.get("_id"))
        del[query_res["_id"]]
        return query_res

    def update_order(self, order_id, order):
        """
        Update an order in the databse

        :param order_id id of order to update
        :param order Order object to replace current order
        """
        column = self.db["orders"]   
        column.update_many({"_id":ObjectId(order_id)},{"$set":order.dictify()})
        return self.get_order(order_id)

    def get_item(self, item) -> dict:
        """
        Retrieve item from warehouse db.

        :param item Item to rerieve
        """

        column = self.db["warehouse"]
        query_res = column.find_one({"item":item},{"_id":0})
        return query_res

    def get_discount(self, cust_type, item) -> int:
        """
        Retrieve discount for customer type for item.
        
        :param cust_type Customer type.
        :param item Item to check for discount.
        """
        column = self.db["discounts"]
        # Get the discount document
        query_res = column.find_one({cust_type : { "$exists": True }})
        # Get the item from the document
        return query_res.get(cust_type).get(item, 0)
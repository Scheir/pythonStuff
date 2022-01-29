# -----------------------------------------------------------
# Order and Order_row are classes that represents an order in
# database.
#
#
# 2021 Andre Scheir Johansson
# email: scheir5@hotmail.se
# -----------------------------------------------------------

from database import db
from customer import Customer
import json
import math

discounts = {
    "Small Company":{
        "pen":10,
        "notebook":10,
        "paper":10,
        "eraser":10
    },
    "Big Company": {
        "pen":30,
        "notebook":10,
        "paper":30,
        "eraser":10
    },
    "Private":{}
}

FREE_BIKE_THRESHOLD = 10000

class Order_row:
    """
    An order row is one row of an article in an order.
    
    Attributes
    ----------
    item: Article in question (pen, paper, etc.)
    qty: Quantity of the item in the order row
    unit_price: Price per article unit
    unit_discount: Discount per unit for the customer
    total_price: total price for the order row
    total_discount: total discount for the order row
    """
    def __init__(self, item, qty, customer, free = False):
        """
        Constructor
        
        :param item Item to create order row for
        :param qty Quantity of item
        :param customer Cutomer associated with the order row
        :param free Is it a free promotion item
        """
        self.item = item
        self.qty = qty
        #Get item and price from db
        db_inst = db.get_instance()
        query = db_inst.get_item(item)

        # During promotion period we can give away free items.
        # So we need to handle that.
        if free:
            # Check if item exist in db
            if not query:
                raise AttributeError
            self.unit_price = 0
            self.unit_discount = 0
            self.total_discount = 0
            self.total_price = 0

        else:
            # Try to querry price, if failed, item doesnt exist in database
            try: 
                self.unit_price = int(query.get("price"))
            except:
                raise AttributeError

            self.unit_discount = db_inst.get_discount(customer.type, item)
            self.total_price = round(self.unit_price * self.qty, 2)
            self.total_discount = round(self.total_price * (self.unit_discount/100), 2)
        
    @classmethod
    def create_free_item(cls, item, customer):
        """
        Class method to construct a bike order row.
        """
        return cls(item, 1, customer, True)
      

    def get_order_row(self):
        """
        Create a dictionary of all the items and their value
        """
        keys = ["item", "unit price", "quantity", "total price", "total discount"]
        values = [self.item, self.unit_price, self.qty, self.total_price, self.total_discount]
        return dict(zip(keys,values))

    def __str__(self):
        return f'item: {self.item}, qty: {self.qty}, price: {self.total_price}, disc: {self.total_discount}'

class Order:
    """
    An Order is the object that represents and Order in DB
    Id is not generated here, it is genereated when stored in DB

    Attributes
    ----------
    customer: Customer linked to the order
    order_list: Array of order_rows
    total_price: Total order price
    total_discount: Total order discount
    failed_items: Items not found in DB
    """
    def __init__(self, customer, cart):
        self.customer = Customer(customer)
        self.failed_items = []
        self.order_list = []
        for item,qty in cart.items():
            # If we fail to append, item doesnt exists in database.
            try:
                self.order_list.append(Order_row(item, qty, self.customer))
            except:
                print("Exception for item:", item)
                self.failed_items.append(item)

        self.total_price = sum(row.total_price for row in self.order_list)
        self.total_discount = sum(row.total_discount for row in self.order_list)

        # Promotions goes here #
        # Add free bike if total price is above threshold
        if self.total_price > FREE_BIKE_THRESHOLD:
            self.order_list.append(Order_row.create_free_item("bike", self.customer))

    def dictify(self):
        """
        Create a dictionary of all attributes for the class.
        Used when storing in DB
        """
        orders = [order.get_order_row() for order in self.order_list]
        order_dict = {
            "customer":self.customer.name,
            "order list":orders,
            "total price":self.total_price,
            "total discount":self.total_discount}
        return order_dict
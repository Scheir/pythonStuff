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

#### PROMOTION FUNCTIONS ####
# Add all promotion functions here

# Free item promotion: get a free item if a threshold is reached
free_item = lambda order_inst, threshold: order_inst.total_price > int(threshold.get("threshold"))

#### PROMOTION FUNCTIONS DICT ###
# add all promotion functions maped with the promotion type here
promotion_funcs = {
    "free item": free_item
    # More potential promotions 
    }

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
        self.check_promotions()
        
        #if self.total_price > FREE_BIKE_THRESHOLD:
         #   self.order_list.append(Order_row.create_free_item("bike", self.customer))

    def check_promotions(self):
        """
        Iterate through all promotion documents in the DB and 
        check if criterias are met and if promotion is active.
        If this is the case, add an order row of the promoted item
        to the order.
        """

        db_inst = db.get_instance()

        # Iterate all promotions we get from DB
        for promo in db_inst.get_promotions():
            # Get the key (type of promotion)
            promo_type = next(iter(promo))
            # Get the values associated with the key
            obj_value = promo.get(promo_type)

            # Extract all fields from the values
            item = obj_value.get("item")
            active = bool(obj_value.get("active"))
            conditions = obj_value.get("conditions")
            
            # All promotion functions are stored in the dictionary
            # promotion_funcs, key is the promo type and value is the function
            # Ex: "free item":free_item
            # conditions is passed as *conditions as some promo functions
            # might need more than 1 parameter.
            if active and promotion_funcs[promo_type](self, *conditions):
                self.order_list.append(Order_row.create_free_item(item, self.customer))
    
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
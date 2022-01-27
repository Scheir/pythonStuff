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
    def __init__(self, item, qty, customer):
        self.item = item
        self.qty = qty
        #TODO: Query price of item
        # Dummy DB for now
        for line in open("/Users/scheir/Desktop/python/pythonStuff/DB/items.txt"):
            item_, price = line.split()
            if item_ == self.item:
                break
        self.unit_price = int(price)
        self.unit_discount = discounts.get(customer.type).get(self.item,0)
        self.total_price = round(self.unit_price * self.qty, 2)
        self.total_discount = round(self.total_price * (self.unit_discount/100), 2)
    
    @classmethod
    def create_bike(cls, customer):
        return cls("bike", 0, customer)
      

    def get_order_row(self):
        keys = ["item", "unit price", "quantity", "total price", "total discount"]
        values = [self.item, self.unit_price, self.qty, self.total_price, self.total_discount]
        return dict(zip(keys,values))


    def __str__(self):
        return f'item: {self.item}, qty: {self.qty}, price: {self.total_price}, disc: {self.total_discount}'


class Order:
    def __init__(self, customer, cart):
        db_inst = db.get_instance()
        self.id = 1 # db_inst.create_order_id()
        self.customer = Customer(customer)
        self.order_list = []
        for item,qty in cart.items():
            self.order_list.append(Order_row(item, qty, self.customer))
        self.total_price = sum(row.total_price for row in self.order_list)
        self.total_discount = sum(row.total_discount for row in self.order_list)
        
        # Add free bike if total price is above threshold
        if self.total_price > FREE_BIKE_THRESHOLD:
            self.order_list.append(Order_row.create_bike(self.customer))

    def dictify(self):
        orders = [order.get_order_row() for order in self.order_list]
        order_dict = {
            "customer":self.customer.name,
            "order list":orders,
            "total price":self.total_price,
            "total discount":self.total_discount}
        return order_dict

        

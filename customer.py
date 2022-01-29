# -----------------------------------------------------------
# The class Customer represents the customer object stored in
# DB.
#
# 2021 Andre Scheir Johansson
# email: scheir5@hotmail.se
# -----------------------------------------------------------

import json
class Customer:
    """
    The Customer object represents the Customers in the DB.
    It has two attributes, name and type.
    """
    def __init__(self, data):
        """
        Constructor
        
        :param data Data Contains fields name and type
        """
        
        self.name = data.get("name")
        self.type = data.get("type")
        
    def dictify(self) -> str:
        """
        Create a dictionary object from the Customer attributes.
        Useful when inserting customer to DB
        """
        return {"name":self.name,"type":self.type}
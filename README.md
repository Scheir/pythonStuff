# pythonStuff

This repo contains a Customer order API, which is a python flask project that uses a mongoDB database.
The API can do the following things:

* Create a new customer
* Query a customer
* Create an order
* Update an order
* Query and order

The endpoint used for create and query customer is /customer.
The endpoint used from create, update and query order is /order

#Examples of API usages.

To create a customer do a POST request to <SERVER>/customer.
The body requires a name and a type field.

{
	"name":"Scheir",
	"type":"Small Company"
}
  
To query a customer do a GET request to <SERVER>/customer.
The body requires a name field
  
{
	"name":"Scheir",
}
  
To create an order do a POST requst to <SERVER>/order.
The body requires name, and a cart: list of valid items and their quantity.
  
{
	"name":"Scheir",
	"cart":[{"pen":1},{"paper":1}]
}

To update an order do a PUT request to <SERVER>/order.
The body requires order id, name and a cart: list of valid items and their quantity.

{
	"id":"61f27a8b506cb23d13d7ac48",
	"name": "Scheir",
	"cart":[{"pen":4},{"eraser":3}]
}

To query an order do a GET request to <SERVER>/order.
The body requires order id.
  
{
	"id":"61f27a8b506cb23d13d7ac48",
}

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

* To create a customer do a POST request to <SERVER>/customer. The body requires a name and a type field.

	* {
	"name":"Scheir",
	"type":"Small Company"
	}
  
* To query a customer do a GET request to <SERVER>/customer. The body requires a name field
  
	* {
	"name":"Scheir",
	}
  
* To create an order do a POST requst to <SERVER>/order.The body requires name, and a cart: list of valid items and their quantity.
  
	* {
	"name":"Scheir",
	"cart":[{"pen":1},{"paper":1}]
	}

* To update an order do a PUT request to <SERVER>/order. The body requires order id, name and a cart: list of valid items and their quantity.

	* {
	"id":"61f27a8b506cb23d13d7ac48",
	"cart":[{"pen":4},{"eraser":3}]
	}

* To query an order do a GET request to <SERVER>/order. The body requires order id.
  
	* {
	"id":"61f27a8b506cb23d13d7ac48",
	}


# Prerequisites 

Mongo DB has to be installed, and the following collections has to be instantiated:
* warehouse - Containing documents of avilable items and their price
* discounts - Containing documents of discount info for all type of customers

Examples of how to initialize these collections:

* Warehouse example containing pen, paper, eraser, notebook and bike:
	* db.warehouse.insert({item:"pen",price:"10"})

	* db.warehouse.insert({item:"paper",price:"100"})

	* db.warehouse.insert({item:"eraser",price:"1000"})

	* db.warehouse.insert({item:"notebook",price:"5000"})

	* db.warehouse.insert({item:"bike",price:"100000"})

	
* Discounts example with 10 % off for Small Companies, and additional 10% on paper and pen for Big Companies, no discound for Private customers:
	
	* db.discounts.insert({"Big Company" : { "pen" : 30, "paper" : 30, "eraser" : 10, "notebook" : 10 } })
	
	* db.discounts.insert({"Small Company" : { "pen" : 10, "paper" : 10, "eraser" : 10, "notebook" : 10 } })
	
	* db.discounts.insert({"Private" : { } })

# How to run (on macOS Catalina)

* Clone the repo
* Create a python env -> python3 -m venv <ENV_NAME>
* Run the virtual environment -> source <ENV_NAME>/bin/activate
* Install the required libraries -> pip install -r requirements.txt
* Run the app -> python3 server.py
* The database server is read from environment variable DBMONGO_SERVER
* The database name is read from environment variable DB_NAME
* If these envronment variables are not set, they will get defualt values.

# -----------------------------------------------------------
# This file contains all JSON-schemas that are used to 
# validat the request bodies in the request handler.
#
#
# 2021 Andre Scheir Johansson
# email: scheir5@hotmail.se
# -----------------------------------------------------------

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

customer_name_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type":"string",
            "pattern": "^[a-zA-Z0-9 ]+$"
        }
    },
    "additionalProperties": False,
    "required": [
    "name",
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

order_update_schema = {
    "type": "object",
    "properties": {
        "id": {
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
        "id",
        "cart"
    ]
}

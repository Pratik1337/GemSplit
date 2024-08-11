BILL_IDENTIFICATION_PROMPT = """
You are given an image of a restaurant bill. Your task is to analyze the bill and extract the following details: 
  - List of items ordered
  - Quantity of each item
  - Price of each item
  - Individual items amount, price multiplied by quantity for each item
  - Total amount
  - Any additional charges (tax, service charge, etc.)
  - Date of the bill
  - Name of the restaurant
  - Type of item (food, alcohol or beverage)
  - Tax mentioned on the bill if applicable and visible (GST, CGST, SGST, IGST etc)

Please provide the extracted information in a structured JSON format as shown below:

{
  'restaurant_name': 'Example Restaurant',
  'date': 'YYYY-MM-DD',
  'items': [
    {
      'item_name': 'Item 1',
      'quantity': 2,
      'price': 10.00,
      'amount': 20.00,
      'item_type': 'Food'
    },
    {
      'item_name': 'Item 2',
      'quantity': 2,
      'price': 5.00,
      'amount': 10.00,
      'item_type': 'Liquor'
    }
  ],
  'additional_charges': {
    'tax': [
            'SGST': {
                'percentage': 2.00,
                'amount': 11.50,
        },
            'CGST': {
                'percentage': 2.00,
                'amount': 11.50,
        },
            'other': {
                'percentage': 1.00,
                'amount': 2.50,
        }
    ]
    'service_charge': 2.00
},
  'total_amount': 23.50
}

If any of the details are not present on the bill, please indicate them as 'Not Available'. Ensure the data is accurate and clearly presented."
Return a JSON object of your response, DO NOT prepend of append any text to the JSON
"""


BILL = """
    "data": {
        "restaurant_name": "Bangalore IDLI CAFE",
        "date": "03/07/24",
        "items": [
            {
                "item_name": "Dahi Vada (2pc)",
                "quantity": 1,
                "price": 120.0,
                "amount": 120.0,
                "item_type": "Food"
            },
            {
                "item_name": "Idli (2pc)",
                "quantity": 1,
                "price": 70.0,
                "amount": 70.0,
                "item_type": "Food"
            },
            {
                "item_name": "Onion Plain Dosa",
                "quantity": 1,
                "price": 100.0,
                "amount": 100.0,
                "item_type": "Food"
            },
            {
                "item_name": "Filter Coffee",
                "quantity": 2,
                "price": 40.0,
                "amount": 80.0,
                "item_type": "Beverage"
            }
        ],
        "additional_charges": {
            "tax": [
                {
                    "percentage": 2.5,
                    "amount": 9.25,
                    "tax_type": "SGST"
                },
                {
                    "percentage": 2.5,
                    "amount": 9.25,
                    "tax_type": "CGST"
                }
            ],
            "service_charge": "Not Available"
        },
        "total_amount": 389.0
    }

"""

BILL_SPLIT_CUSTOM_REQUEST = f"""
This food bill was shared between 3 people. Alice, Bob and John. Split the bill among 3 people. 
Alice ate only Dahi Vada, while Bob and John ate everything else. Split the bill intelligently. 
"""

BILL_CALCULATE_RESULT_EXAMPLE = """
[
    {
        "name": "Alice",
        "amount": "125"
    },
    {
        "name": "Bob",
        "amount": "175"
    },
    {
        "name": "John",
        "amount": "214"
    }
]
"""

BILL_CALCULATION_PROMPT = f"""
You will be given JSON data of a bill, along with image of the actual bill. 
example of a bill data that you will get : {BILL}
Your task is to split the bill according to the custom request provided by the user. 
The Users request is : {BILL_SPLIT_CUSTOM_REQUEST}

Identify the Parties/People from the users request and calculate the exact share that each person from the user request has to pay.
You response must be a JSON object and it must only contain the Party/Person and their respective share in the bill split.
Example of output: {BILL_CALCULATE_RESULT_EXAMPLE}
"""
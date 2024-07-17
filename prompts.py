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

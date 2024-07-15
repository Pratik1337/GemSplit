import base64
import json
import os
import shutil
import uuid

from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import APIRouter, UploadFile, File
import requests
from PIL import Image
import io
import re

from starlette.responses import JSONResponse

router = APIRouter(
    prefix='/api/v1/gemai',
    tags=['Gemini AI']
)


load_dotenv()

api_key = os.environ.get('GOOGLE_API_KEY')

genai.configure(api_key=api_key)


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
  - Type of item (food or alcohol)

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
    'tax': 1.50,
    'service_charge': 2.00
  },
  'total_amount': 23.50
}

If any of the details are not present on the bill, please indicate them as 'Not Available'. Ensure the data is accurate and clearly presented."
Return a JSON object of your response, DO NOT prepend of append any text to the JSON
"""

# def image_url_to_byte_array(image_path):
#     print("UPLOADING IMAGE ")
#     sample_file = genai.upload_file(path="/Users/pratikbarde/Downloads/bill001.jpeg",display_name="nike shoe")
#     print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
#     file = genai.get_file(name=sample_file.name)
#     print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")
#
#     model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
#
#     response = model.generate_content([sample_file, BILL_IDENTIFICATION_PROMPT])
#     # print(response.text)
#     json_response = response.text
#     return json_response

# image_data = image_url_to_byte_array(image_url)
# content = genai.Content(data=image_data, mime_type="image/png")
# response = model.generate_content(prompt="Identify the product in the image. Describe it", content=content)


def generate_digital_bill(image_path, image_name):
    print("UPLOADING IMAGE ")
    sample_file = genai.upload_file(path=image_path, display_name=image_name)
    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    response = model.generate_content([sample_file, BILL_IDENTIFICATION_PROMPT])

    json_response = extract_json_from_response(response.text)

    print("RESPONSE IS ", response)
    return json_response


def extract_json_from_response(response_text: str) -> dict:
    # Clean the JSON string
    json_str = response_text.strip().replace("'", '"').replace('\n', '').replace('\t', '').replace('\r', '')
    return json.loads(json_str)


@router.post("/bill/")
async def upload_image(file: UploadFile = File(...)):
    try:
        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)

        original_filename = file.filename

        name, ext = os.path.splitext(original_filename)
        short_uuid = str(uuid.uuid4())[:8]
        new_filename = f"{name}_{short_uuid}{ext}"
        file_path = os.path.join(temp_dir, new_filename)

        print("FILE NAME IS ", new_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        response_object = generate_digital_bill(file_path, new_filename)

        os.remove(file_path)

        return JSONResponse(content={"message": "Bill image processed successfully", "data": response_object})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)






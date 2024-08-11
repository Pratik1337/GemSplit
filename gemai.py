import json
import os
import shutil
import uuid

from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import APIRouter, UploadFile, File
from fastapi import Request
from starlette.responses import JSONResponse
import prompts
from bill_processor.digital_bill_processor import DigitalBillProcessor

router = APIRouter(
    prefix='/api/v1/gemai',
    tags=['Gemini AI']
)


load_dotenv()

api_key = os.environ.get('GOOGLE_API_KEY')

genai.configure(api_key=api_key)

dbp = DigitalBillProcessor()



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

    response = model.generate_content([sample_file, prompts.BILL_IDENTIFICATION_PROMPT])

    json_response = extract_json_from_response(response.text)

    print("RESPONSE IS ", response)
    return json_response


def extract_json_from_response(response_text: str) -> dict:
    # Clean the JSON string
    json_str = response_text.strip().replace("'", '"').replace('\n', '').replace('\t', '').replace('\r', '')
    return json.loads(json_str)


@router.post("/bill")
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

        uploaded_image_file = dbp.upload_image(file_path, new_filename)
        response_object = dbp.generate_digital_bill(uploaded_image_file)

        os.remove(file_path)

        return JSONResponse(content={"message": "Bill image processed successfully", "data": response_object})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/bill/calculate")
async def print_data(request: Request):
    try:
        # Asynchronously get JSON data from request body
        data = await request.json()
        print("Received data:", data)
        data_json = data['data']
        print("DATA JSON",str(data_json))

        combined_json = str(data_json) + "\n" + prompts.BILL_SPLIT_CUSTOM_REQUEST + "\n" + prompts.BILL_CALCULATION_PROMPT
        result = dbp.calculate_split(combined_json)
        # Return a response to confirm data receipt
        # result = str(result)
        # result = dbp.extract_json_from_response(result)
        return JSONResponse(content={"message": "Data received successfully", "data": result})
    except Exception as e:
        # Handle exceptions that may occur during data retrieval and parsing
        print(f"An error occurred: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

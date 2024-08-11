import json
import os
import shutil
import uuid
import prompts
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import APIRouter, UploadFile, File


class DigitalBillProcessor:
    def __init__(self):
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    def upload_image(self, image_path, image_name):
        print("UPLOADING IMAGE")
        image_file = genai.upload_file(path=image_path, display_name=image_name)
        print(f"Uploaded file '{image_file.display_name}' as: {image_file.uri}")
        return image_file

    def generate_digital_bill(self, sample_file):
        file = genai.get_file(name=sample_file.name)
        print(f"Retrieved file '{file.display_name}' as: {file.uri}")

        response = self.model.generate_content([sample_file, prompts.BILL_IDENTIFICATION_PROMPT])
        json_response = self.extract_json_from_response(response.text)

        print("RESPONSE IS ", response)
        return json_response

    def extract_json_from_response(self,response_text: str) -> dict:
        # Clean the JSON string
        json_str = response_text.strip().replace("'", '"').replace('\n', '').replace('\t', '').replace('\r', '').replace("`", '')
        return json.loads(json_str)

    def calculate_split(self, bill_prompt):
        try:

            print("BILL PROMPT COMBINED", bill_prompt)

            # response = self.model.generate_content([bill_prompt])
            response = self.model.generate_content(bill_prompt)
            # json_response = self.extract_json_from_response(response.text)
            return response.text

            # json_response = self.extract_json_from_response(response.text)
            #
            # print("RESPONSE IS ", json_response)
            # return json_response
            # Check if the response object has the expected attributes
            # if hasattr(response, 'text'):
            #     # Extract JSON from the response text
            #     json_response = self.extract_json_from_response(response.text)
            #     print("Response JSON:", json_response)
            #     return json_response
            # else:
            #     print("Unexpected response format:", response)
            #     return None

        except json.JSONDecodeError:
            print("Invalid JSON input")
            return {"error": "Invalid JSON input"}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": str(e)}
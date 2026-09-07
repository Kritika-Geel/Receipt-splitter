from google import genai
from PIL import Image
from schemas import BillData
import os
import streamlit as st

# Automatically pulls from .streamlit/secrets.toml locally, or Streamlit Cloud in production
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def parse_receipt(image: Image.Image) -> BillData:
    prompt = """
    You are an expert OCR and bill-parsing assistant.
    Analyze the uploaded restaurant receipt photo and extract:
    1. Every line item with its name, quantity, total price, and your extraction confidence score (0.0 to 1.0).
    2. The subtotal before taxes.
    3. Total GST/VAT/taxes.
    4. Service charge or tip.
    5. Any discounts applied.
    6. The final total printed on the receipt.

    Be precise with decimals. If any fee/discount is absent, set it to 0.0.
    """
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[image, prompt],
        config={
            "response_mime_type": "application/json",
            "response_schema": BillData,
        },
    )
    return BillData.model_validate_json(response.text)
from pydantic import BaseModel, Field
from typing import List

class LineItem(BaseModel):
    name: str = Field(description="Name of the food or beverage item")
    quantity: int = Field(default=1, description="Quantity of the item")
    price: float = Field(description="Total price for this line item")
    confidence: float = Field(default=1.0, description="Confidence score between 0.0 and 1.0")

class BillData(BaseModel):
    subtotal: float = Field(description="Sum of all items before taxes and fees")
    service_charge: float = Field(default=0.0, description="Service charge or tip amount")
    gst_tax: float = Field(default=0.0, description="Total GST / VAT / Sales tax")
    discount: float = Field(default=0.0, description="Total discount applied")
    total_printed: float = Field(description="Final total printed on the receipt")
    items: List[LineItem] = Field(description="List of all individual items on the bill")
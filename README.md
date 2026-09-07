# Proportional Bill Splitter

A Streamlit web application that converts restaurant receipt photos into itemized, mathematically fair bill splits.

Splitting a check evenly penalizes diners who ordered lighter items, while manual splitting becomes tedious once discounts, service charges, and taxes come into play. This project automates receipt parsing, provides an interactive human-in-the-loop review interface, and divides all extra fees strictly as a proportion of each person's actual consumption.

---

### Key Features

* **Multimodal OCR Extraction:** Automatically extracts line items, quantities, unit prices, taxes, service charges, and discounts using Google's Gemini Vision models (`gemini-2.5-flash`).
* **Confidence Scoring & Verification:** Displays confidence metrics for extracted lines and flags arithmetic discrepancies when the printed total doesn't match the calculated sum.
* **Human-in-the-Loop Review:** Allows diners to edit misread dish names, modify prices, or manually add missing items before finalizing.
* **Flexible Assignments:** Supports assigning line items to single individuals, custom subgroups sharing dishes, or split evenly table-wide.
* **Proportional Math Engine:** Apportions taxes, service fees, and discounts based on each diner's share of the food subtotal rather than flat division.

---

### Project Structure

```text
receipt-splitter/
├── .streamlit/
│   └── secrets.toml       # Local API credentials (git-ignored)
├── test_receipts/         # Test dataset (crumpled, thermal, angled, dim light)
├── app.py                 # Streamlit UI & interactive review interface
├── extractor.py           # Gemini multimodal OCR parsing logic
├── splitter.py            # Proportional distribution math engine
├── schemas.py             # Pydantic data validation schemas
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignored environment and secret files
└── README.md              # Project documentation

```

---

### Tech Stack

* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **Vision Model:** Google Gemini API (`google-genai`)
* **Validation:** Pydantic (v2)
* **Image Handling:** Pillow (PIL)

---

### Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Kritika-Geel/receipt-splitter.git
cd receipt-splitter

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configure API credentials:**
Create a `.streamlit/secrets.toml` file in the root directory:
```toml
GEMINI_API_KEY = "AIzaSyYourActualAPIKeyHere"

```


4. **Run the application:**
```bash
python -m streamlit run app.py

```


The application will be accessible at `http://localhost:8501`.

---

### Test Receipt Dataset

The `test_receipts/` directory contains 12 sample bills covering edge cases:

* Clean flat printed bills
* Faded thermal paper receipts
* Crumpled and creased paper
* Off-angle and perspective-distorted shots
* Low-light / cast shadows
* Printed math discrepancy samples (triggers validation warning)

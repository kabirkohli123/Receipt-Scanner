import re
from datetime import datetime

# ---------------------------
# 1) Extract Vendor / Company
# ---------------------------

def extract_vendor(text):
    lines = text.split("\n")
    vendor = None

    # Common vendor indicators
    keywords = [
        "restaurant", "hotel", "hospital", "store", "mart", "pharmacy",
        "supermarket", "medical", "clinic", "food", "invoice", "bill"
    ]

    # First 5 lines usually contain vendor name
    for line in lines[:5]:
        clean = line.strip()
        if len(clean) > 3 and not clean.isdigit():
            # ignore lines with random OCR garbage
            if any(k.lower() in clean.lower() for k in keywords):
                vendor = clean
                break

    # fallback – use first non-empty line
    if not vendor:
        for line in lines:
            if len(line.strip()) > 3:
                vendor = line.strip()
                break

    return vendor


# ---------------------------
# 2) Extract Date
# ---------------------------

def extract_date(text):
    patterns = [
        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}/\d{2}/\d{2}",
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}-\d{2}-\d{4}",
        r"\d{2}-\d{2}-\d{2}",
        r"\w+ \d{1,2}, \d{4}",   # January 10, 2024
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return match.group()

    return None


# ---------------------------
# 3) Extract Amount (Enhanced)
# ---------------------------

def extract_amount(text):
    clean = text.replace(",", "")

    priority_patterns = [
        r"Total\s*[:\-]?\s*\₹?\s*(\d+\.\d+|\d+)",
        r"Grand\s*Total\s*[:\-]?\s*\₹?\s*(\d+\.\d+|\d+)",
        r"Amount\s*Payable\s*[:\-]?\s*\₹?\s*(\d+\.\d+|\d+)",
        r"Net\s*Amount\s*[:\-]?\s*\₹?\s*(\d+\.\d+|\d+)",
        r"Bill\s*Amount\s*[:\-]?\s*\₹?\s*(\d+\.\d+|\d+)",
        r"Payable\s*[:\-]?\s*(\d+\.\d+|\d+)",
    ]

    for p in priority_patterns:
        matches = re.findall(p, clean, flags=re.IGNORECASE)
        if matches:
            return float(matches[-1])  # last is usually final

    # Fallback — pick largest number (excluding phone numbers)
    numbers = re.findall(r"\b\d+\.\d+|\b\d+", clean)
    valid = [float(n) for n in numbers if 0 < float(n) < 200000]
    if valid:
        return max(valid)

    return None


# ---------------------------
# 4) Extract Invoice Number
# ---------------------------

def extract_invoice(text):
    patterns = [
        r"Invoice\s*No[:\-]?\s*(\w+)",
        r"Bill\s*No[:\-]?\s*(\w+)",
        r"INVOICE\s*#\s*(\w+)",
        r"T\.?No[:\-]?\s*(\w+)",
    ]

    for p in patterns:
        match = re.search(p, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)

    return None


# ---------------------------
# 5) Extract GST / Tax Amount
# ---------------------------

def extract_tax(text):
    matches = re.findall(r"GST\s*[:\-]?\s*(\d+\.\d+|\d+)", text, flags=re.IGNORECASE)
    if matches:
        return float(matches[-1])
    return None


# ---------------------------
# 6) Extract Payment Method
# ---------------------------

def extract_payment_method(text):
    methods = {
        "cash": ["cash", "paid cash"],
        "card": ["card", "credit", "debit", "visa", "mastercard"],
        "upi": ["upi", "gpay", "paytm", "phonepe"],
    }

    lower = text.lower()

    for method, keywords in methods.items():
        if any(k in lower for k in keywords):
            return method.capitalize()

    return "Unknown"


# ---------------------------
# FINAL PARSE FUNCTION
# ---------------------------

def parse(text):
    return {
        "vendor": extract_vendor(text),
        "date": extract_date(text),
        "amount": extract_amount(text),
        "invoice_number": extract_invoice(text),
        "tax": extract_tax(text),
        "payment_method": extract_payment_method(text),
        "raw_text": text
    }

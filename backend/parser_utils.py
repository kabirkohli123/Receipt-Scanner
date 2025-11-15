import re

def parse(text):
    data = {
        "vendor": None,
        "date": None,
        "amount": None,
        "invoice_number": None,
        "category": "Medical",
        "raw_text": text
    }

    # ------ Extract Vendor (First line with letters + spaces) ------
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if lines:
        # First meaningful line is usually vendor / hospital / shop name
        data["vendor"] = lines[0]

    # ------ Date Extraction ------
    date_patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",    # 12/09/2024
        r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",    # 12-09-2024
        r"\b\d{4}-\d{2}-\d{2}\b",          # 2024-10-01
        r"\b\d{1,2} [A-Za-z]{3,9} \d{2,4}\b" # 12 Sept 2024
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            data["date"] = match.group()
            break

    # ------ Amount Extraction (Total, Amount due, Paid, etc.) ------
    amount_patterns = [
        r"Total[:\s]*\$?(\d+\.\d{2})",
        r"Amount[:\s]*\$?(\d+\.\d{2})",
        r"Balance[:\s]*\$?(\d+\.\d{2})",
        r"Due[:\s]*\$?(\d+\.\d{2})",
        r"\$([\d,]+\.\d{2})"     # $123.45
    ]

    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amt = match.group(1).replace(",", "")
            data["amount"] = float(amt)
            break

    # ------ Invoice Number Extraction ------
    invoice_patterns = [
        r"Invoice[:\s]*([A-Za-z0-9-]+)",
        r"Invoice No[:\s]*([A-Za-z0-9-]+)",
        r"Inv[:\s]*([A-Za-z0-9-]+)"
    ]

    for pattern in invoice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["invoice_number"] = match.group(1)
            break

    # ------ Category Detection ------
    if "hospital" in text.lower() or "medical" in text.lower():
        data["category"] = "Medical"
    elif "restaurant" in text.lower():
        data["category"] = "Food"
    elif "grocery" in text.lower():
        data["category"] = "Grocery"
    elif "invoice" in text.lower():
        data["category"] = "Invoice"

    # Default vendor if empty
    if not data["vendor"]:
        data["vendor"] = "Unknown Vendor"

    return data

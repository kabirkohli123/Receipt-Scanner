import cv2
import os
import pytesseract
from PIL import Image
import numpy as np

# Path for Windows Tesseract installation (edit if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(input_path):
    """
    Preprocess image for OCR: resize, grayscale, denoise, threshold.
    Returns processed image output path.
    """

    img = cv2.imread(input_path)

    if img is None:
        print("[ERROR] Could not load image:", input_path)
        return None

    # --- 1. Enlarge small or low-resolution images ---
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # --- 2. Convert to grayscale ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 3. Remove noise ---
    gray = cv2.bilateralFilter(gray, 11, 75, 75)

    # --- 4. Adaptive threshold for text ---
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    # Save processed image
    base, ext = os.path.splitext(input_path)
    output_path = base + "_pre" + ext

    cv2.imwrite(output_path, thresh)

    return output_path


def extract_text_from_image(image_path):
    """
    Full OCR pipeline: preprocess + Tesseract extraction.
    Returns extracted text.
    """

    processed_path = preprocess_image(image_path)

    if processed_path is None:
        return "Error: Image preprocessing failed."

    # Tesseract config for accuracy
    config = "--oem 3 --psm 6"

    try:
        pil_img = Image.open(processed_path)
        text = pytesseract.image_to_string(pil_img, lang="eng", config=config)
        return text.strip()

    except Exception as e:
        return f"Error during OCR: {str(e)}"

from PIL import Image
import pytesseract
import cv2
import re
import os
import io
import base64
import numpy as np

# === TESSERACT CONFIGURATION ===

import pytesseract
import shutil

# Automatically find tesseract path if available
if shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 1 -l hin'

# === TEXT CLEANING FUNCTION ===
def clean_text(text):
    text = re.sub(r'[^ऀ-ॿa-zA-Z0-9\s।,!?%():\-–—"“”‘’\'\n]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# === OCR FOR BASE64 IMAGE INPUT ===
def extract_text_from_base64(base64_str):
    try:
        image_data = base64.b64decode(base64_str)
        image_np = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, config=custom_config)
        return clean_text(text)
    except Exception as e:
        return f"Error in OCR: {str(e)}"

# === OCR FOR LOCAL IMAGE FOLDER ===
def extract_news_bodies_from_images(image_folder="news_images"):
    image_files = sorted([f for f in os.listdir(image_folder)
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    all_texts = []

    for img_name in image_files:
        img_path = os.path.join(image_folder, img_name)
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, config=custom_config)
        cleaned = clean_text(text)
        all_texts.append(cleaned)

    return all_texts

# === BATCH OCR ENTRY POINT FOR BASE64 ===
def process_base64_images(base64_list):
    return [extract_text_from_base64(b64) for b64 in base64_list]

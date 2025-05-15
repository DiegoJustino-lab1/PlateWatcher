# CV3T.py (otimizado recognize_plate)
import cv2
import pytesseract
import numpy as np
import re

# Use Tesseract rápido e modo de página uniforme
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
TESSERACT_CONFIG = "--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"

# Limites de área mínima/máxima de contorno para reduzir falsos positivos
MIN_AREA = 3000
MAX_AREA = 30000

def recognize_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)  # Desfoque bilateral
    edged = cv2.Canny(blur, 30, 200)  # Ajuste os limites do Canny

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 1000 or area > 50000:  # Ajuste os limites de área
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (w*2, h*2))  # Aumenta para melhorar o OCR
            _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            text = pytesseract.image_to_string(thresh, config=TESSERACT_CONFIG)
            text = re.sub(r'[^A-Z0-9-]', '', text).strip()
            if re.match(r'^[A-Z]{3}-\d{4}$', text) or re.match(r'^[A-Z]{3}\d{1}[A-Z]{1}\d{2}$', text):
                return text
    return None

import cv2
import pytesseract
import numpy as np
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
TESSERACT_CONFIG = "--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
MIN_AREA = 300
MAX_AREA = 30000

def recognize_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blur, 20, 200)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA or area > MAX_AREA:
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (w*4, h*4))
            _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            text = pytesseract.image_to_string(thresh, config=TESSERACT_CONFIG)
            text = text.upper().strip()
            print(f"Tesseract OCR bruto: {repr(text)}")

            # Tenta pegar placa completa direto (carro/caminhão)
            cleaned = re.sub(r'[^A-Z0-9-]', '', text)
            if re.fullmatch(r'[A-Z]{3}-?\d{4}', cleaned) or re.fullmatch(r'[A-Z]{3}\d{1}[A-Z]{1}\d{2}', cleaned):
                print("Placa direta (Tesseract):", cleaned)
                return cleaned

            # Tenta separar por linhas (placa de moto)
            linhas = [re.sub(r'[^A-Z0-9]', '', l) for l in text.split('\n') if l.strip()]
            letras = ''
            numeros = ''
            for parte in linhas:
                if re.fullmatch(r'[A-Z]{3}', parte):
                    letras = parte
                elif re.fullmatch(r'\d{4}', parte) or re.fullmatch(r'\d{1}[A-Z]{1}\d{2}', parte):
                    numeros = parte
                elif re.fullmatch(r'[A-Z]{3}\d{4}', parte):
                    print("Placa combinada (Tesseract):", parte)
                    return parte
            if letras and numeros:
                placa = letras + numeros
                print("Placa combinada (Tesseract):", placa)
                return placa
    return None
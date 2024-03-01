#opencv
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\Tesseract.exe"

# Inicia a captura de vídeo da câmera padrão (geralmente a webcam do laptop)
cap = cv2.VideoCapture(0)

# Abre o arquivo dados.csv em modo de anexação
with open("dados.csv", "a") as arquivo:
    while True:
        # Captura um único frame
        ret, frame = cap.read()

        # Se o frame foi capturado corretamente, ret é True
        if ret:
            # Processa o frame com o Tesseract
            resultado = pytesseract.image_to_string(frame)

            if resultado != "":
                print("Texto detectado:")
                print(resultado)

                # Escreve o resultado no arquivo
                arquivo.write(resultado + "\n")

            # Mostra o frame na janela
            cv2.imshow('Camera', frame)

        # Se a tecla 'q' for pressionada, sai do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Libera os recursos da câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
# app.py
from flask import Flask, render_template, Response, jsonify
import cv2
from CV3T import recognize_plate
import time
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Configura a resolução da câmera (pode testar 320x240 se precisar de mais FPS)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Conexão com o MongoDB Atlas
client = MongoClient(
    'mongodb+srv://grupoupx:minhasenha123@cluster0.1ezhthk.mongodb.net/'
    '?retryWrites=true&w=majority&appName=Cluster0'
)
db = client['reconhecimento_placas']
collection = db['placas_detectadas']

# Thread pool para inserções assíncronas
executor = ThreadPoolExecutor(max_workers=2)
frame_count = 0
last_plate = None

def save_plate_to_db(plate):
    data = {
        "placa": plate,
        "data_hora": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    collection.insert_one(data)

def save_plate_to_db_async(plate):
    executor.submit(save_plate_to_db, plate)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global last_plate, frame_count
    while True:
        success, frame = camera.read()
        if not success:
            break

        # redimensiona para performance
        frame = cv2.resize(frame, (640, 480))
        frame_count += 1

        plate = None
        # rodar OCR a cada 15 frames
        if frame_count % 15 == 0:
            plate = recognize_plate(frame)

        if plate and plate != last_plate:
            last_plate = plate
            save_plate_to_db_async(plate)
            cv2.putText(
                frame,
                f"Placa: {plate}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

        ret, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
        time.sleep(0.03)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/last_plate')
def get_last_plate():
    return jsonify({'plate': last_plate})

@app.route('/get_all_plates')
def get_all_plates():
    plates = list(collection.find({}, {"_id": 0}))
    return jsonify(plates)

if __name__ == '__main__':
    app.run(debug=False)

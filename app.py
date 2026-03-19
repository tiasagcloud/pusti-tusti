from flask import Flask, render_template, request, jsonify
import pandas as pd
import cv2
import numpy as np
import base64
from pyzbar.pyzbar import decode
import face_recognition

app = Flask(__name__)

df = pd.read_excel("students.xlsx")

# Convert base64 to image
def base64_to_image(base64_string):
    img_data = base64.b64decode(base64_string.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

# STEP 1: QR Verification
@app.route('/verify_qr', methods=['POST'])
def verify_qr():
    data = request.json['image']
    img = base64_to_image(data)

    decoded = decode(img)
    for obj in decoded:
        qr_data = obj.data.decode('utf-8')
        student = df[df['qr_data'] == qr_data]

        if not student.empty:
            student = student.iloc[0]
            return jsonify({
                "status": "success",
                "id": int(student['id']),
                "name": student['name'],
                "face_path": student['face_image']
            })

    return jsonify({"status": "fail"})

# STEP 2: Face Verification
@app.route('/verify_face', methods=['POST'])
def verify_face():
    data = request.json['image']
    student_id = request.json['id']

    input_img = base64_to_image(data)

    student = df[df['id'] == int(student_id)].iloc[0]
    stored_img = face_recognition.load_image_file("static/" + student['face_image'])

    input_enc = face_recognition.face_encodings(input_img)
    stored_enc = face_recognition.face_encodings(stored_img)

    if len(input_enc) == 0 or len(stored_enc) == 0:
        return jsonify({"status": "no_face"})

    match = face_recognition.compare_faces([stored_enc[0]], input_enc[0])

    if match[0]:
        return jsonify({"status": "verified"})
    else:
        return jsonify({"status": "not_verified"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os

app = Flask(__name__)

EMOTIONS = ['angry', 'contempt', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

model = tf.keras.models.load_model('emotion_recognition_model.h5')

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(48, 48),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face = gray[y:y+h, x:x+w]
    else:
        face = gray
    
    face = cv2.resize(face, (48, 48))
    
    face = face.astype('float32') / 255.0
    
    face = np.expand_dims(face, axis=-1)
    face = np.expand_dims(face, axis=0)
    
    return face

@app.route("/", methods=['GET'])
def home():
    return "아주 성공!"

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['image']
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            
            os.makedirs('uploads', exist_ok=True)
            file.save(filepath)

            processed_image = preprocess_image(filepath)

            predictions = model.predict(processed_image)
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])

            result = {
                'emotion': EMOTIONS[predicted_class],
                'confidence': confidence
            }

            os.remove(filepath)

            return jsonify(result), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
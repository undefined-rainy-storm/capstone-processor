from flask import request
from flask_restful import Resource
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from ..models.emotion import Emotions
from ..services.image_processor import ImageProcessor

class Query(Resource):
    def __init__(self):
        self.image_processor = ImageProcessor()
        
    def get(self):
        return {
            'status': 'ok',
            'timestamp': datetime.now().isoformat()
        }
    
    def post(self):
        try:
            if 'image' not in request.files:
                return {
                    'status': 'error',
                    'timestamp': datetime.now().isoformat(),
                    'message': 'Image not found'
                }, 400

            file = request.files['image']
            filename = secure_filename(file.filename)
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            
            file.save(filepath)
            
            processed_image = self.image_processor.preprocess_image(filepath)
            predicted_class, confidence = self.image_processor.predict(processed_image)
            
            os.remove(filepath)
            
            return {
                'status': 'ok',
                'timestamp': datetime.now().isoformat(),
                'result': list(Emotions)[predicted_class].value,
                'confidence': confidence
            }, 200
            
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'message': str(e)
            }, 500
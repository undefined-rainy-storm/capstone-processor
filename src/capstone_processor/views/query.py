import base64
from io import BytesIO
from PIL import Image
from flask import request
from flask_restful import Resource
from datetime import datetime
import os

from ..models.emotion import Emotions
from ..services.image_processor import ImageProcessor

# RGBA 이미지를 RGB로 변환하는 함수
def convert_rgba_to_rgb(image):
    if image.mode == "RGBA":
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[3])
        return background
    return image

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
            # JSON 데이터에서 base64 이미지를 읽어옴
            data = request.get_json()
            if 'image' not in data:
                return {
                    'status': 'error',
                    'timestamp': datetime.now().isoformat(),
                    'message': 'Image data not found'
                }, 400

            # base64 디코딩
            image_data = data['image']
            try:
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
            except Exception as e:
                return {
                    'status': 'error',
                    'timestamp': datetime.now().isoformat(),
                    'message': 'Invalid base64 image data'
                }, 400
            
            # RGBA 이미지를 RGB로 변환
            image = convert_rgba_to_rgb(image)

            # 임시 파일 경로 생성 및 저장
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, 'temp_image.jpg')
            image.save(filepath)

            # 이미지 처리 및 예측
            processed_image = self.image_processor.preprocess_image(filepath)
            print("Processed image shape:", processed_image.shape) 

            predicted_class, confidence = self.image_processor.predict(processed_image)
            print("Predicted class:", predicted_class)

            # 임시 파일 삭제
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
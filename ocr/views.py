from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import base64
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
class OCRView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            # Get base64 image from request
            image_data = request.data['image']
            image_bytes = base64.b64decode(image_data.split(',')[-1])
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Preprocess (grayscale + resize for better accuracy)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            # OCR with Tesseract
            extracted_text = pytesseract.image_to_string(gray)

            return Response({"text": extracted_text.strip()})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import base64
import cv2
import numpy as np
import easyocr

# Load the model once at startup (not per request)
reader = easyocr.Reader(['en'], gpu=False)  # disable GPU for Render

class OCRView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            image_data = request.data['image']
            image_bytes = base64.b64decode(image_data.split(',')[-1])
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # preprocess
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            # Use pre-loaded reader
            results = reader.readtext(gray)
            texts = [text for _, text, _ in results]

            return Response({"text": texts})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

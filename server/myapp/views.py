# # backend/views.py
# from django.http import JsonResponse
# from firebase_admin import firestore

# def fetch_collection_data(request, document):
#     db = firestore.client()
#     try:
#         # Retrieve documents from the specified Firestore collection
#         doc = db.collection('adafruit_data').document(document)
#         data = {doc.id: doc}
#         print(data)
#         return JsonResponse(data, safe=False)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)


from django.shortcuts import render
from django.http import JsonResponse
from firebase_admin import firestore
import firebase_admin


def home(request):
    # Render the index.html template
    return render(request, 'index.html')

# # Firestore Initialization
# if not firebase_admin._apps:
#     cred = credentials.Certificate('path/to/your/firebase-key.json')
#     firebase_admin.initialize_app(cred)

# db = firestore.client()

def get_data(request, data_type):
    """
    Fetches data from Firestore based on the data type.
    Args:
        request (HttpRequest): The request object.
        data_type (str): Type of data to fetch (e.g., 'temperature', 'humidity').
        
    """
    db = firestore.client()

    try:
        doc_ref = db.collection('adafruit_data').document(data_type)
        doc = doc_ref.get()
        if doc.exists:
            data_array = doc.to_dict().get('data')  # Assuming the data is stored under 'data' key in document
            formatted_data = [
                {'created_at': item['created_at'], 'value': item['value']} for item in data_array
            ]
            return JsonResponse(formatted_data, safe=False)
        else:
            return JsonResponse({'error': 'Document does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

# views.py
import requests
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json

logger = logging.getLogger(__name__)  # Set up logging

@csrf_exempt
@require_http_methods(["POST"])
def toggle_led(request):
    try:

        # data = request.json() if hasattr(request, 'json') else request.POST
        data = json.loads(request.body.decode('utf-8'))
        print("DATA =  ", data)
        value = data.get('value')   
        headers = {
            'X-AIO-Key': settings.ADAFRUIT_IO_KEY,
            'Content-Type': 'application/json'
        }
        payload = {'value': value}
        response = requests.post(f'https://io.adafruit.com/api/v2/{settings.ADAFRUIT_IO_USERNAME}/feeds/led/data', json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return JsonResponse({'status': 'success', 'data': response.json()})
    except Exception as e:
        logger.exception("Failed to toggle LED")  # Logs the error with traceback
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



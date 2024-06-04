# myapp/apps.py
from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials


## Load Config of Firebase project
from decouple import config
GOOGLE_APPLICATION_CREDENTIALS = config('GOOGLE_APPLICATION_CREDENTIALS')

## Test Status Connection to firebase
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError

def test_firestore_connection():
    db = firestore.client()
    try:
        # Attempt to fetch a document from a known collection
        doc_ref = db.collection('test_collection').document('test_document')
        doc = doc_ref.get()
        if doc.exists:
            print("Connection to Firebase Successfully: Document retrieved successfully.")
            print("Document data:", doc.to_dict())
        else:
            print("Connection to Firebase Successfully: Document does not exist, but connection was successful.")
    except FirebaseError as e:
        print("Failed to connect to Firestore:", str(e))
    except Exception as e:
        print("An error occurred:", str(e))


class MyAppConfig(AppConfig):
    name = 'myapp'
    verbose_name = 'My Application'
    debug = False
    
    def ready(self):

        cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
        firebase_admin.initialize_app(cred)
        test_firestore_connection()

        import threading
        from .subscribe import start_redis_subscription
        # thread = threading.Thread(target=start_redis_subscription)
        # thread.daemon = True
        # thread.start()
        start_redis_subscription()


        from .mqtt_client import mqtt_init
        client = mqtt_init()
        print("MQTT client running. Listening for messages...")

        if self.debug:
            import logging
            logging.basicConfig(level=logging.DEBUG)

            client.enable_logger()  # Call this before connecting to get detailed logs from Paho

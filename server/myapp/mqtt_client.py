
import paho.mqtt.client as mqtt
import ssl
import requests
from .redis_config import get_redis_client
from firebase_admin import firestore
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

#you need to create your own adafruit key, and paste that key in this
ADAFRUIT_IO_USERNAME_THANG = ""
ADAFRUIT_IO_USERNAME_VUONG = ''

ADAFRUIT_IO_KEY_VUONG = '' 
ADAFRUIT_IO_KEY_THANG = ''

ADAFRUIT_IO_USERNAME = ADAFRUIT_IO_USERNAME_THANG
ADAFRUIT_IO_KEY = ADAFRUIT_IO_KEY_THANG

FEEDKEY_THANG = ["temperature", "humidity", "light", "led"]
FEEDKEY_VUONG = ['hk232-da-temp', 'hk232-da-hum','hk232-da-light','hk232-da-led','hk232-da-history','hk232-da-face','hk232-da-voice','hk232-da-ledcontrol']
FEEDKEY = FEEDKEY_THANG


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
    else:
        if rc == 5:
            print("Connection refused - not authorized. Check your username and AIO Key.")
        else:
            print("Connection failed with code %d." % rc)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for feedkey in FEEDKEY: 
        client.subscribe(f"{ADAFRUIT_IO_USERNAME}/feeds/{feedkey}")

def create_websocket():
    pass
    
def on_subscribe( client , userdata , mid , granted_qos ) :
    print ("Subcribe Topic successfully ...")

def on_message(client, userdata, msg):
    
    print(f"Message received on topic {msg.topic} with payload {msg.payload.decode()}")
    # Determine which feed was updated
    feed_key = msg.topic.split('/')[-1]  # Assuming topic format is 'username/feeds/feed_key'
    db = firestore.client()
    redis_client = get_redis_client()
    print(f"Checking Status of Redis server:   {redis_client.ping()}")

    channel_layer = get_channel_layer()
    print(channel_layer)
    async_to_sync(channel_layer.group_send)(
        'data_group',
        {
            'type': 'data.message',
            'message': {
                'topic': feed_key,
                'msg': msg.payload.decode()
            }
        }
    )

    # Fetch the latest data for this feed
    url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{feed_key}/data/last"
    headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        latest_data = response.json()
        # Save this data to Firestore
        doc_ref = db.collection('adafruit_data').document(feed_key)

        # Firestore transaction to ensure atomicity
        @firestore.transactional
        def update_in_transaction(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)
            if snapshot.exists:
                # Append to the existing array
                transaction.update(doc_ref, {
                    'data': firestore.ArrayUnion([{
                        'value': latest_data['value'],
                        'created_at': latest_data['created_at']
                    }])
                })
            else:
                # Create the document with initial data
                transaction.set(doc_ref, {
                    'data': [{
                        'value': latest_data['value'],
                        'created_at': latest_data['created_at']
                    }]
                })

        # Start a Firestore transaction
        transaction = db.transaction()
        update_in_transaction(transaction, doc_ref)


        redis_client.set(f"{feed_key}", latest_data['value'])
        # Publish the latest data to a Redis Pub/Sub channel
        redis_client.publish(f'{feed_key}', f"Updated {feed_key} with value {latest_data['value']}")

        print(f"Data saved to Firestore for feed {feed_key}")
    else:
        print(f"Failed to fetch data from Adafruit IO for feed {feed_key}")


def on_publish(client, userdata, mid):
    print("Message Published!")


def publish_data(client, feed_key, value):
    topic = f"{ADAFRUIT_IO_USERNAME}/feeds/{feed_key}"
    result = client.publish(topic, value)

    if result[0] == 0:
        print(f"Send `{value}` to topic `{topic}` successfully.")
    else:
        print(f"Failed to send message to topic {topic}")

def disconnected ( client ) :
    import sys

    print ("Disconnecting AdaFruitIO ...")
    sys.exit(1)


def mqtt_init():

    client = mqtt.Client()
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    client.tls_set_context(ssl.create_default_context())
    client.connect("io.adafruit.com", 8883, 60)
    client.loop_start()

    
    return client



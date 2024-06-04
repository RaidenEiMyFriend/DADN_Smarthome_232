from .redis_config import get_redis_client

def handle_message(message):
    print("Received message:", message['data'])

def start_redis_subscription():
    redis_client = get_redis_client()
    pubsub = redis_client.pubsub()
    pubsub.subscribe(**{'temperature': handle_message})

    print("Subscribed to channel 'temperature'. Listening for messages...")
    #pubsub.run_in_thread(sleep_time=0.001)

from fastapi import FastAPI
import redis

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# 1. Define a clean callback handler for incoming messages
def my_handler(message):
    print(f"Message received: {message['data'].decode('utf-8')}")

# 2. Setup your subscription channel mapping
pubsub = redis_client.pubsub()
pubsub.subscribe(**{"my-channel": my_handler})

# 3. Spin up the background worker thread seamlessly
thread = pubsub.run_in_thread(sleep_time=0.001, daemon=True)

@app.post("/publish/{message}")
async def publish_message(message: str):
    redis_client.publish("my-channel", message)
    return {"status": "Message has been published"}

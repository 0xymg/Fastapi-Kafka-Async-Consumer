import os
import ssl
import asyncio
from contextlib import asynccontextmanager
from aiokafka import AIOKafkaConsumer
import redis.asyncio as aioredis  # use redis-py's async support
from fastapi import FastAPI
from dotenv import load_dotenv
import json

load_dotenv()

# Kafka broker details
KAFKA_SERVER = os.environ["SERVERS"]
KAFKA_USERNAME = os.environ["USERNAME2"]
KAFKA_PASSWORD = os.environ["PASSWORD"]
KAFKA_GROUP_ID = os.environ["GROUP_ID"]

# Redis configuration
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_DB = os.environ["REDIS_DB"]
# Set a TTL for the Kafka message in Redis (in seconds). After 1 hour messages will be removed
TTL_SECONDS = 3600

# Create an async Redis client
redis_client = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

#If you don't know what you are doing, dont touch this!!!
ssl_context = ssl.create_default_context()


async def consume_kafka():
    consumer = AIOKafkaConsumer(
        "KAFKA_TOPIC...",
        bootstrap_servers=KAFKA_BROKER_URL,
        sasl_mechanism="PLAIN",
        security_protocol="SASL_SSL",
        ssl_context=ssl_context,
        group_id=KAFKA_GROUP_ID,
        sasl_plain_username=KAFKA_USERNAME,
        sasl_plain_password=KAFKA_PASSWORD,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Received: {msg.value}")
            # Store the message in Redis asynchronously
            await redis_client.setex(f"kafka_message:{msg.offset}", TTL_SECONDS, json.dumps(msg.value))
    finally:
        await consumer.stop()


# FASTAPI STARTUP EVENT
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Kafka Consumer task
    task = asyncio.create_task(consume_kafka())
    yield #means finally in FastAPI
    # Ensure the task is cancelled on shutdown
    task.cancel()
    await task
    # Close Redis connection on shutdown
    await redis_client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Kafka data processing is running in the background."}


#To see  
@app.get("/redis-data")
async def get_redis_data():
    keys = await redis_client.keys("kafka_message:*")
    data = {}
    for key in keys:
        value = await redis_client.get(key)
        data[key.decode("utf-8")] = json.loads(value.decode("utf-8"))
    return data


#Remove Redis Data in current db
@app.get("/flush-db")
async def flush_redis_db():
    await redis_client.flushdb()
    return ({"message": f"Redis --database {REDIS_DB}-- flushed successfully."})

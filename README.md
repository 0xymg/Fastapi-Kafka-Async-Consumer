# FastAPI Kafka Redis Async Consumer and Async Storager

## Overview

This project demonstrates how to consume messages from a Kafka using FastAPI. It asynchronously processes messages and stores them in Redis.

## Requirements

- Python 3.7+
- FastAPI
- Kafka
- Redis

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0xymg/Fastapi-Kafka-Async-Consumer.git
   ```
   
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for Kafka and Redis configuration in a `.env` file.
   ```bash
   ## KAFKA CONFIGURATIONS 
   USERNAME2=''
   PASSWORD=  ''
   SERVERS=''
   GROUP_ID=''
   ## REDIS CONFIGURATIONS
   REDIS_HOST=''
   REDIS_PORT=6379
   REDIS_DB = 0 ## 0...15
   ```
## Running the Application

To run the FastAPI server, execute the following command:
```bash
uvicorn main:app --reload
```

## Features

- Asynchronous Kafka message consumption.
- Stores messages asynchronously in Redis with a time-to-live (TTL).
- FastAPI endpoints to view and flush data in Redis.



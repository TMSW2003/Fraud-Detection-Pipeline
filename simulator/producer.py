import json
import os
import random
import time
from confluent_kafka import Producer, KafkaError, Message
from typing import Optional


from transactions import generate_transactions
from create_users import create_user_profiles

BROKER = os.getenv("BROKER", "localhost:19092")
TOPIC = "transactions"
NUM_USERS = 100
SEND_DELAY_SECONDS = 0.25

def delivery_report(err: Optional[KafkaError], msg: Message) -> None:
    '''Handle the delivery result for a message sent to Kafka/Redpanda.'''
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to {msg.topic()} "
            f"partition {msg.partition()} "
            f"offset {msg.offset()}"
        )

producer = Producer({
    "bootstrap.servers": BROKER
})

topic = TOPIC

rng = random.Random(42)  # Set fixed seed for reproducibility
user_list = create_user_profiles(NUM_USERS, rng) 

count = 0

# Generate transactions and produce them to Kafka/Redpanda topic
for txn in generate_transactions(user_list, rng): 
    producer.produce(
        topic,
        key=txn["user_id"].encode("utf-8"),
        value=json.dumps(txn).encode("utf-8"),
        callback=delivery_report
    )

    producer.poll(0)  # Trigger delivery callback for previous messages
    time.sleep(SEND_DELAY_SECONDS) 

    count += 1
    print(f"Produced {txn['transaction_id']} for {txn['user_id']}")

producer.flush()

print(f"Finished sending {count} transactions.")
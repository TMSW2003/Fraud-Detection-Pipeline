import json
import os
from confluent_kafka import Consumer, KafkaException


TOPIC = "transactions"
GROUP_ID = "fraud-detector-dev"
BROKER = os.getenv("BROKER", "localhost:19092")

consumer = Consumer({
    "bootstrap.servers": BROKER,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest",
})

consumer.subscribe([TOPIC]) #receive messages from the transactions topic

print(f"Listening for messages on topic: {TOPIC}")


# Continuously poll for new messages and process them
try:
    while True:
        msg = consumer.poll(1.0) #Wait for a message for up to 1 second

        if msg is None:
            continue

        if msg.error():
            raise KafkaException(msg.error())

        #malformed messages are skipped and error logged but don't stop consumer
        try:
            txn = json.loads(msg.value().decode("utf-8")) #Deserialize message value from JSON format

            print(
                f"Consumed {txn['transaction_id']} | "
                f"user={txn['user_id']} | "
                f"amount={txn['amount']} | "
                f"fraud={txn['is_fraud']} | "
                f"type={txn['fraud_type']} | "
                f"partition={msg.partition()} | "
                f"offset={msg.offset()}"
            )
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError) as e:
            print(
                f"Skipping malformed message at "
                f"partition={msg.partition()} offset={msg.offset()}: {e}"
            )
            continue


except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()
import json
import pika
from app.core.config import settings


def publish(queue_name: str, payload: dict) -> None:
    params = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(payload).encode(),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


def publish_imu_review(payload: dict) -> None:
    publish("imu.doctor.review", payload)


def publish_stp(payload: dict) -> None:
    publish("stp.case.update", payload)

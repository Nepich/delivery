from kafka import KafkaProducer

from infrastructure.adapters.kafka.out.kafka_contract_pb2 import OrderStatusChangedIntegrationEvent
from infrastructure.adapters.postgres.entities.event import Event


class KafkaBus:
    def __init__(
        self, 
        servers: list[str],
        ):
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
        )
        self.mappings = {}

    def register_topic(self, event: Event, topic: str):
        self.mappings[event.__name__] = topic
        
    async def publish(self, event: Event):
        contract_message = OrderStatusChangedIntegrationEvent(
            orderId=event.content.get("order_id"),
            orderStatus=event.content.get("status").capitalize()
            )
        topic = self.mappings.get(event.event_type)
        self.producer.send(topic=topic, value=contract_message.SerializeToString(), key=event.id.bytes)
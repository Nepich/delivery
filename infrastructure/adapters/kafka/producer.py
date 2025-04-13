from typing import Any

from kafka import KafkaProducer

from api.mediator import Mediator
from infrastructure.adapters.kafka.out.kafka_contract_pb2 import OrderStatusChangedIntegrationEvent



class KafkaBus:
    def __init__(
        self, 
        servers: list[str],
        event_topics: tuple[tuple[Any, str]],
        mediator: Mediator
        ):
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
        )
        self.mappings = {event_topic[0].__name__:event_topic[1] for event_topic in event_topics}
        self.mediator = mediator

    async def publish(self, event: Any):
        contract_message = OrderStatusChangedIntegrationEvent(
            orderId=event.order_id,
            orderStatus=event.status
            )
        topic = self.mappings.get(event.__name__)
        self.producer.send(topic=topic, value=contract_message.SerializeToString(), key=event.id)
    
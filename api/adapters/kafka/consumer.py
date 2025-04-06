import asyncio
import json
from kafka import KafkaConsumer
from that_depends import Provide

from api.adapters.kafka.out.contract_pb2 import BasketConfirmedIntegrationEvent
from api.dic import DIContainer
from api.mediator import Mediator
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand


class Consumer:
    def __init__(
        self, 
        topics: list[str], 
        servers: list[str], 
        mediator: Mediator = Provide[DIContainer.mediator.sync_resolve()]
        ):
        print("==============", servers, "================", sep="\n")
        self.consumer = KafkaConsumer(
            bootstrap_servers=servers,
            value_deserializer=lambda m: json.loads(m.decode('ascii'))
        )
        self.topics = topics
        self.mediator = mediator

    def process(self):
        self.consumer.subscribe(*self.topics)
        print(self.consumer.subscription())
        while True:
            for msg in self.consumer:
                event = BasketConfirmedIntegrationEvent(**msg)
                print(event)
                command = CreateOrderCommand(
                    basket_id=event.basketId,
                    street=event.address.street
                    )
                asyncio.run(self.mediator.notify(command=command))
                
                
                

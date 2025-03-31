from typing import Protocol

from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand


class ICreateOrderHandler(Protocol):
    
    async def handle(self, command: CreateOrderCommand):
        ...
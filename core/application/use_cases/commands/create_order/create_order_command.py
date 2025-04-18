from pydantic import BaseModel
from uuid import UUID

from core.primitives.icommand import Command


class CreateOrderCommand(BaseModel, Command):
    basket_id: UUID
    street: str
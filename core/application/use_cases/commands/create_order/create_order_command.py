from pydantic import BaseModel
from uuid import UUID


class CreateOrderCommand(BaseModel):
    basket_id: UUID
    street: str
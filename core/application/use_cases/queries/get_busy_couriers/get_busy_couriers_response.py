from uuid import UUID
from pydantic import BaseModel, Field


class LocationResponse(BaseModel):
    x: int
    y: int
    

class GetBusyCouriersResponse(BaseModel):
    id: UUID
    name: str
    location: LocationResponse
    transport_id: UUID
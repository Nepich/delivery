from uuid import UUID
from pydantic import BaseModel


class LocationResponse(BaseModel):
    x: int
    y: int
    

class GetIncompletedOrdersResponse(BaseModel):
    id: UUID
    location: LocationResponse
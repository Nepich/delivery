from dataclasses import dataclass, field
from uuid import UUID, uuid4

from core.domain.courier_aggregate.courier_status import CourierStatus
from core.domain.shared_kernel.location import Location
from core.domain.courier_aggregate.transport import Transport
from core.domain.courier_aggregate.courier_status import CourierStatus
from core.domain.shared_kernel.location import Location


@dataclass
class Courier:
    name: str
    _transport: Transport
    _location: Location
    _status: CourierStatus
    _id: UUID
    
    @property
    def transport(self):
        return self._transport

    @property
    def id(self):
        return self._id
        
    @property
    def location(self):
        return self._location
    
    @property
    def status(self):
        return self._status
    
    def __init__(
        self, 
        name: str, 
        transport_name: str, 
        transport_speed: int, 
        location: Location
        ):
        if not (isinstance(name, str) and isinstance(transport_name, str)):
            raise TypeError("name and transport_name should be type of string")
        if not isinstance(transport_speed, int):
            raise TypeError("transport_speed should be type of int")
        if not isinstance(location, Location):
            raise TypeError("location should be type of Location")
        if not (name and transport_name and transport_speed and location):
            raise ValueError(
                "name, transport_name, transport_speed, location should be not empty or empty string"
                )
        
        self._id = uuid4()
        self.name = name
        self._transport = Transport(name=transport_name, speed=transport_speed)
        self._location = location
        self._status = CourierStatus.FREE

    def __eq__(self, other_courier: "Courier"):
        return self._id == other_courier.id

    def set_busy(self):
        if self._status == CourierStatus.BUSY:
            raise Exception("this courier is already busy")
        self._status = CourierStatus.BUSY

    def set_free(self):
        if self._status == CourierStatus.FREE:
            raise Exception("this courier is already free")
        self._status = CourierStatus.FREE
        
    def move(self, destination: Location):
        if not isinstance(destination, Location):
            raise TypeError("destination should be type of Location")
        new_location = self._transport.move(
            current=self.location, destination=destination
            )
        self._location = new_location
        
    def time_to_location(self, destination: Location) -> float:
        if not isinstance(destination, Location):
            raise TypeError("destination should be type of Location")        
        
        distance = self._location.distance(destination=destination)
        return distance / self._transport.speed
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
    __transport: Transport
    __location: Location
    __status: CourierStatus
    __id: UUID
    
    @property
    def transport(self):
        return self.__transport

    @property
    def id(self):
        return self.__id
        
    @property
    def location(self):
        return self.__location
    
    @property
    def status(self):
        return self.__status
    
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
        
        self.__id = uuid4()
        self.name = name
        self.__transport = Transport(name=transport_name, speed=transport_speed)
        self.__location = location
        self.__status = CourierStatus.FREE()

    def __eq__(self, other_courier: "Courier"):
        return self.__id == other_courier.id

    def set_busy(self):
        busy = CourierStatus.BUSY()
        if self.__status == busy:
            raise Exception("this courier is already busy")
        self.__status = busy

    def set_free(self):
        free = CourierStatus.FREE()
        if self.__status == free:
            raise Exception("this courier is already free")
        self.__status = free
        
    def move(self, destination: Location):
        if not isinstance(destination, Location):
            raise TypeError("destination should be type of Location")
        new_location = self.__transport.move(
            current=self.location, destination=destination
            )
        self.__location = new_location
        
    def time_to_location(self, destination: Location) -> float:
        if not isinstance(destination, Location):
            raise TypeError("destination should be type of Location")        
        
        distance = self.__location.distance(destination=destination)
        return distance / self.__transport.speed
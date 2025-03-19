from dataclasses import dataclass, field
from uuid import UUID

from core.domain.order_aggregate.order_status import OrderStatus
from core.domain.shared_kernel.location import Location


@dataclass
class Order:
    __id: UUID
    __location: Location
    __status: OrderStatus
    __courier_id: UUID

    @property
    def id(self):
        return self.__id
        
    @property
    def location(self):
        return self.__location

    @property
    def status(self):
        return self.__status
    
    @property
    def courier_id(self):
        return self.__courier_id
        
    def __init__(self, id: UUID, location: Location):
        if not isinstance(id, UUID):
            raise TypeError("id should be type of UUID")
        if not isinstance(location, Location):
            raise TypeError("location should be type of Location")
        
        self.__id = id
        self.__location = location
        self.__status = OrderStatus.CREATED()
        self.__courier_id = None

    def assign(self, courier_id: UUID):
        if not isinstance(courier_id, UUID):
            raise TypeError("courier_id should be type of UUID")
        
        if self.__status != OrderStatus.CREATED():
            raise Exception("this order is already assigned")
        
        self.__courier_id = courier_id
        self.__status = OrderStatus.ASSIGNED()

    def complete(self):
        if self.__status != OrderStatus.ASSIGNED():
            raise Exception("this order hasn't been assigned yet")
        
        self.__status = OrderStatus.COMPLETED()
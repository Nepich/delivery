from collections import deque
from dataclasses import dataclass
from uuid import UUID

from core.domain.order_aggregate.domain_events.order_finished_event import OrderFinishedEvent
from core.domain.order_aggregate.order_status import OrderStatus
from core.domain.shared_kernel.location import Location


@dataclass
class Order:
    _id: UUID
    _location: Location
    _status: OrderStatus
    _courier_id: UUID | None
    __events: deque[OrderFinishedEvent]

    @property
    def id(self):
        return self._id
        
    @property
    def location(self):
        return self._location

    @property
    def status(self):
        return self._status
    
    @property
    def courier_id(self):
        return self._courier_id
        
    def __init__(self, id: UUID, location: Location):
        if not isinstance(id, UUID):
            raise TypeError("id should be type of UUID")
        if not isinstance(location, Location):
            raise TypeError("location should be type of Location")
        
        self._id = id
        self._location = location
        self._status = OrderStatus.CREATED
        self._courier_id = None

    def __eq__(self, other_order: "Order"):
        return self._id == other_order.id
    
    def assign(self, courier_id: UUID):
        if not isinstance(courier_id, UUID):
            raise TypeError("courier_id should be type of UUID")
        
        if self._status != OrderStatus.CREATED:
            raise Exception("this order is already assigned")
        
        self._courier_id = courier_id
        self._status = OrderStatus.ASSIGNED

    def complete(self):
        if self._status != OrderStatus.ASSIGNED:
            raise Exception("this order hasn't been assigned yet")
        
        self._status = OrderStatus.COMPLETED
        self.__raise_domain_event(
            OrderFinishedEvent(order_id=self._id, status=self._status)
            )
        
    def __raise_domain_event(self, event: OrderFinishedEvent) -> None:
        self.__events.append(event)
        
    def clear_domain_events(self) -> None:
        self.__events.clear()
        
    def get_domain_events(self) -> deque[OrderFinishedEvent]:
        return self.__events
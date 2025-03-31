import math

from core.domain.courier_aggregate.courier_status import CourierStatus
from core.domain.order_aggregate.order_status import OrderStatus
from core.domain.courier_aggregate.courier import Courier
from core.domain.order_aggregate.order import Order


class DispatchService:
    
    def dispatch(self, order: Order, couriers: list[Courier]) -> Courier:
        if not (order and couriers):
            raise ValueError("order and couriers could not be empty")
        if not isinstance(order, Order):
            raise TypeError("order should be type of order")
        if not (
            isinstance(couriers, list) 
            and all(map(lambda x: isinstance(x, Courier), couriers))
            ):
            raise TypeError("order should be type of order")
        if order.status != OrderStatus.CREATED:
            raise Exception("only order with status created can be dispatched")

        free_status = CourierStatus.FREE
        best_match = math.inf
        best_courier = None
        for courier in couriers:
            if courier.status != free_status:
                continue
            
            time_to_order = courier.time_to_location(destination=order.location)
            if time_to_order < best_match:
                best_match = time_to_order
                best_courier = courier
        
        if not best_courier:
            raise Exception("no suited courier")
        
        order.assign(best_courier.id)
        best_courier.set_busy()
        
        return best_courier

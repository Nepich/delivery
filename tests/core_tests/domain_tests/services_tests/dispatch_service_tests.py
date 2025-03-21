from uuid import uuid4
import pytest
from core.domain.courier_aggregate.courier import Courier
from core.domain.courier_aggregate.courier_status import CourierStatus
from core.domain.order_aggregate.order import Order
from core.domain.order_aggregate.order_status import OrderStatus
from core.domain.services.dispatch_service import DispatchService
from core.domain.services.idispatch_service import IDispatchService
from core.domain.shared_kernel.location import Location


class DispatchServiceShould:
    service: IDispatchService = DispatchService()

    @pytest.mark.parametrize(
        "order,couriers",
        [
            (
                Order(id=uuid4(), location=Location(9,9)), 
                [
                    Courier(name="Ivan", transport_name="bmw", transport_speed=1, location=Location(3,3)),
                    Courier(name="Fedor", transport_name="audi", transport_speed=3, location=Location(2,2))
                ]
            ),
        ]
    )
    def be_dispatched(self, order: Order, couriers: list[Courier]):
        best_courier = self.service.dispatch(order=order, couriers=couriers)
        assert best_courier.name == "Fedor"
        assert best_courier.transport.name == "audi"
        assert best_courier.status == CourierStatus.BUSY()
        assert order.status == OrderStatus.ASSIGNED()
        
    @pytest.mark.parametrize(
        "order,couriers,error",
        [
            (
                Order(id=uuid4(), location=Location(9,9)), 
                [
                    Courier(name="Ivan", transport_name="bmw", transport_speed=1, location=Location(3,3)),
                    "123"
                ],
                TypeError
            ),
            (
                "123", 
                [
                    Courier(name="Ivan", transport_name="bmw", transport_speed=1, location=Location(3,3)),
                    Courier(name="Fedor", transport_name="audi", transport_speed=3, location=Location(2,2))
                ],
                TypeError           
            ),
            (
                Order(id=uuid4(), location=Location(9,9)), 
                [],
                ValueError                
            )
        ]
    )
    def not_be_dispatched_because_of_type_errors(self, order: Order, couriers: list[Courier], error):
        with pytest.raises(error):
            self.service.dispatch(order=order, couriers=couriers)
        
    @pytest.mark.parametrize(
        "order,couriers,error",
        [
            (
                Order(id=uuid4(), location=Location(9,9)), 
                [
                    Courier(name="Ivan", transport_name="bmw", transport_speed=1, location=Location(3,3)),
                    Courier(name="Fedor", transport_name="audi", transport_speed=3, location=Location(2,2))
                ],
                Exception
            ),
        ]
    )
    def not_be_dispatched_because_of_order_error(self, order: Order, couriers: list[Courier], error):
        with pytest.raises(error):
            order.assign(courier_id=uuid4())
            self.service.dispatch(order=order, couriers=couriers)
            
    @pytest.mark.parametrize(
        "order,couriers,error",
        [
            (
                Order(id=uuid4(), location=Location(9,9)), 
                [
                    Courier(name="Ivan", transport_name="bmw", transport_speed=1, location=Location(3,3)),
                    Courier(name="Fedor", transport_name="audi", transport_speed=3, location=Location(2,2))
                ],
                Exception
            ),
        ]
    )
    def not_be_dispatched_because_of_courier_error(self, order: Order, couriers: list[Courier], error):
        with pytest.raises(error):
            for courier in couriers:
                courier.set_busy()
            self.service.dispatch(order=order, couriers=couriers)
from uuid import UUID, uuid4
import pytest

from core.domain.order_aggregate.order import Order
from core.domain.order_aggregate.order_status import OrderStatus
from core.domain.shared_kernel.location import Location


class OrderShould:
    @pytest.mark.parametrize(
        "id,location",
        [
            (uuid4(), Location(1,1)),
        ]
    )
    def be_initialized_correct(
        self, 
        id: UUID, 
        location: Location
        ):
        order = Order(
            id=id,
            location=location
            )
        assert isinstance(order, Order)
        assert order.id == id
        assert order.status == OrderStatus.CREATED()
        assert order.courier_id == None
        assert order.location == location
        assert isinstance(order.id, UUID)
        
    @pytest.mark.parametrize(
        "id,location,error",
        [
            ("", Location(1,1), TypeError),
            (uuid4(), "", TypeError),
        ]
    )
    def not_be_initialized(
        self, 
        id: UUID, 
        location: Location,
        error,
        ):
        with pytest.raises(error):
            Order(
                id=id,
                location=location
                )

    @pytest.mark.parametrize(
        "order,courier_id",
        [
            (Order(uuid4(), Location(1,1)), uuid4()),
        ]
    )
    def be_assigned(
        self, 
        order: Order, 
        courier_id: UUID
        ):
        order.assign(courier_id=courier_id)
        assert order.status == OrderStatus.ASSIGNED()
        
    @pytest.mark.parametrize(
        "order,courier_id,error",
        [
            (Order(uuid4(), Location(1,1)), "", TypeError),
            (Order(uuid4(), Location(1,1)), uuid4(), Exception),
        ]
    )
    def not_be_assigned(
        self, 
        order: Order, 
        courier_id: UUID,
        error
        ):
        with pytest.raises(error):
            order.assign(courier_id=courier_id)
            order.assign(courier_id=courier_id)

    @pytest.mark.parametrize(
        "order,courier_id",
        [
            (Order(uuid4(), Location(1,1)), uuid4()),
        ]
    )
    def be_completed(
        self, 
        order: Order, 
        courier_id: UUID
        ):
        order.assign(courier_id=courier_id)
        order.complete()
        assert order.status == OrderStatus.COMPLETED()
        
    @pytest.mark.parametrize(
        "order,error",
        [
            (Order(uuid4(), Location(1,1)), Exception),
        ]
    )
    def not_be_completed(
        self, 
        order: Order, 
        error
        ):
        with pytest.raises(error):
            order.complete()
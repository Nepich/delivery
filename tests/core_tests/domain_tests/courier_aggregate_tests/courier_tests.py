from uuid import UUID
import pytest

from core.domain.courier_aggregate.courier import Courier
from core.domain.courier_aggregate.courier_status import CourierStatus
from core.domain.shared_kernel.location import Location


class CourierShould:
    @pytest.mark.parametrize(
        "name,transport_name,transport_speed,location",
        [
            ("Bill", "audi", 2, Location(1,1)),
            ("Jim", "bmw", 3, Location(2,3))
        ]
    )
    def be_initialized_correct(
        self, 
        name: str, 
        transport_name: str, 
        transport_speed: int, 
        location: Location
        ):
        courier = Courier(
            name=name,
            transport_name=transport_name,
            transport_speed=transport_speed,
            location=location
            )
        assert isinstance(courier, Courier)
        assert courier.name == name
        assert courier.transport.name == transport_name
        assert courier.transport.speed == transport_speed
        assert courier.location == location
        assert isinstance(courier.id, UUID)
        
    @pytest.mark.parametrize(
        "name,transport_name,transport_speed,location,error",
        [
            ("", "audi", 2, Location(1,1), ValueError),
            (123, "audi", 2, Location(1,1), TypeError),
            ("Bill", "", 2, Location(1,1), ValueError),
            ("Bill", 123, 2, Location(1,1), TypeError),
            ("Bill", "audi", "some_str", Location(1,1), TypeError),
            ("Bill", "audi", 10, Location(1,1), ValueError),
            ("Bill", "audi", 2, 123, TypeError),
        ]
    )
    def not_be_initialized(
        self, 
        name: str, 
        transport_name: str, 
        transport_speed: int, 
        location: Location,
        error,
        ):
        with pytest.raises(error):
            Courier(
                name=name,
                transport_name=transport_name,
                transport_speed=transport_speed,
                location=location
                )

    @pytest.mark.parametrize(
        "courier",
        [
            Courier("Bill", "audi", 2, Location(1,1)),
        ]
    )
    def be_set_busy_correct(self, courier: Courier):
        courier.set_busy()
        assert courier.status == CourierStatus.BUSY()
        
    @pytest.mark.parametrize(
        "courier,error",
        [
            (Courier("Bill", "audi", 2, Location(1,1)), Exception),
        ]
    )
    def not_be_set_busy_correct(self, courier: Courier, error):
        courier.set_busy()
        with pytest.raises(error):
            courier.set_busy()
            
    @pytest.mark.parametrize(
        "courier",
        [
            Courier("Bill", "audi", 2, Location(1,1)),
        ]
    )
    def be_set_free_correct(self, courier: Courier):
        courier.set_busy()
        courier.set_free()
        assert courier.status == CourierStatus.FREE()
        
    @pytest.mark.parametrize(
        "courier,error",
        [
            (Courier("Bill", "audi", 2, Location(1,1)), Exception),
        ]
    )
    def not_be_set_free_correct(self, courier: Courier, error):
        with pytest.raises(error):
            courier.set_free()
            
    @pytest.mark.parametrize(
        "courier, destination",
        [
            (Courier("Bill", "audi", 2, Location(1,1)), Location(7,7)),
        ]
    )
    def be_moved(self, courier: Courier, destination: Location):
        courier.move(destination)
        assert 1 <= courier.location.x <= 3
        assert 1 <= courier.location.y <= 3
        
    @pytest.mark.parametrize(
        "courier,destination,error",
        [
            (Courier("Bill", "audi", 2, Location(1,1)), "", TypeError),
        ]
    )
    def not_be_moved(self, courier: Courier, destination: Location, error):
        with pytest.raises(error):
            courier.move()
            
    @pytest.mark.parametrize(
        "courier,destination, time_to_location",
        [
            (Courier("Bill", "audi", 2, Location(1,1)), Location(7,7), 6.0),
            (Courier("Bill", "audi", 1, Location(1,1)), Location(7,7), 12.0),
        ]
    )
    def be_count_time_to_location(self, courier: Courier, destination: Location, time_to_location: float):
        time = courier.time_to_location(destination=destination)
        assert time == time_to_location
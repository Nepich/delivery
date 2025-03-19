from copy import deepcopy
from uuid import UUID
import pytest

from core.domain.shared_kernel.location import Location
from core.domain.courier_aggregate.transport import Transport


class TransportShould:

    @pytest.mark.parametrize(
        "name,speed",
        [
            ("audi", 1),
            ("bmw", 2)
        ]
    )
    def be_initialized_correct(self, name: str, speed: int):
        transport = Transport(name=name,speed=speed)
        assert isinstance(transport, Transport)
        assert transport.name == name
        assert transport.speed == speed
        assert isinstance(transport.id, UUID)
        
    @pytest.mark.parametrize(
        "name,speed,error",
        [
            ("", 1, ValueError),
            (1, 1, TypeError),
            (1, "audi", TypeError),
            ("1", "audi", TypeError),
            ("audi", 1.1, TypeError),
            ("audi", 0, ValueError),
            ("audi", 7, ValueError),
        ]
    )
    def not_be_initialized(self, name: str, speed: int, error: Exception):
        with pytest.raises(error):
            Transport(name=name,speed=speed)
            
    def be_equal(self):
        first_transport = Transport(name="audi", speed=2)
        second_transport = deepcopy(first_transport)
        assert first_transport == second_transport
            
    def not_be_equal(self):
        first_transport = Transport(name="audi", speed=2)
        second_transport = Transport(name="audi", speed=2)
        assert first_transport != second_transport
            
    @pytest.mark.parametrize(
        "transport,current,destination",
        [
            (Transport("audi", 2), Location(1,1), Location(4,5)),
            (Transport("audi", 3), Location(1,1), Location(2,2)),
        ]
    )            
    def be_moved(self, transport: Transport, current: Location, destination: Location):
        new_location = transport.move(current=current, destination=destination)
        assert isinstance(new_location, Location)
        assert new_location != current
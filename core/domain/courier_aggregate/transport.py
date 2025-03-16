from dataclasses import dataclass, field
from uuid import UUID, uuid4

from core.domain.shared_kernel.location import Location


@dataclass
class Transport:
    id: UUID = field(init=False, default_factory=uuid4)
    name: str
    speed: int
    
    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("name could be only type of str")
        if not isinstance(self.speed, int):
            raise TypeError("speed could be only type of int")
        if not self.name:
            raise ValueError("name could not be empty")
        if not (1 <= self.speed <= 3):
            raise ValueError("speed could not be less then 1 or greater then 3")
    
    def __eq__(self, other_transport: "Transport"):
        return self.id == other_transport.id
    
    def move(self, current: Location, destination: Location) -> Location:
        if not (isinstance(current, Location) and isinstance(destination, Location)):
            raise TypeError("current and destination should be type of Location")
        
        cruising_range = self.speed
        dif_x = destination.x - current.x
        dif_y = destination.y - current.y
        move_x = max(-cruising_range, min(cruising_range, dif_x))
        cruising_range -= abs(move_x)
        move_y = max(-cruising_range, min(cruising_range, dif_y))
        return Location(x=current.x+move_x, y=current.y+move_y)
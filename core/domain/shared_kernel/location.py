from dataclasses import dataclass
from random import randint


@dataclass(frozen=True)
class Location:
    x: int
    y: int
    
    def __post_init__(self):
        if not (isinstance(self.x, int) and isinstance(self.y, int)):
            raise TypeError(f"Type of X={type(self.x)}; Type of Y={type(self.y)}!!!\nX and Y should be type int")
        if self.x < 1 or self.y < 1:
            raise ValueError(f"X={self.x}; Y={self.y}!!!\nX and Y should be greater then 0")
        if self.x > 10 or self.y > 10:
            raise ValueError(f"X={self.x}; Y={self.y}!!!\nX and Y should be less then 10")
        
    def __eq__(self, other: "Location"):
        return (
            True if self.x == other.x and self.y == other.y 
            else False
            )
        
    def distance(self, destination: "Location"):
        x_steps = self.x - destination.x if self.x >= destination.x else destination.x - self.x
        y_steps = self.y - destination.y if self.y >= destination.y else destination.y - self.y
        return x_steps + y_steps
    
    @classmethod
    def random(cls):
        return cls(x=randint(1,10), y=randint(1,10))
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CourierStatus:
    def __new__(cls):
        raise TypeError("Cannot create CourierStatus directly. Use classmethods BUSY, FREE")        
    
    @classmethod
    def __create(cls, name):
        instance = super().__new__(cls)
        object.__setattr__(instance, "name", name)
        return instance
        
    @classmethod
    def BUSY(cls):
        return cls.__create("busy")

    @classmethod
    def FREE(cls):
        return cls.__create("free")

    def __eq__(self, other_status: "CourierStatus") -> bool:
        return self.name == other_status.name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
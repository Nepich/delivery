from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class OrderStatus:
    def __new__(cls):
        raise TypeError("Cannot create OrderStatus directly. Use classmethods CREATED, ASSIGNED, COMPLETED")        
    
    @classmethod
    def __create(cls, name):
        instance = super().__new__(cls)
        object.__setattr__(instance, "name", name)
        return instance
        
    @classmethod
    def CREATED(cls):
        return cls.__create("created")

    @classmethod
    def ASSIGNED(cls):
        return cls.__create("assigned")
    
    @classmethod
    def COMPLETED(cls):
        return cls.__create("completed")

    def __eq__(self, other_status: "OrderStatus") -> bool:
        return self.name == other_status.name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
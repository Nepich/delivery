from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(kw_only=True)
class DomainEvent:
    id: UUID = field(default_factory=uuid4)
    
    def as_dict(self) -> dict:
        return {
            "id": str(self.id),
            "event_type": self.__class__.__name__,
            "content": {
                k:str(v) if isinstance(v, UUID) else v 
                for k,v in self.__dict__.items()
                },
        }
    
    @staticmethod
    def uuid_serialization(obj):
        if isinstance(obj, UUID):
            return str(obj)
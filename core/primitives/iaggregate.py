from dataclasses import dataclass

from core.primitives.idomain_event import DomainEvent


@dataclass(kw_only=True)
class Aggregate:
    _events: list[DomainEvent]
    
    @property
    def events(self):
        return self._events
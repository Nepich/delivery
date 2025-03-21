
from that_depends import BaseContainer, providers

from core.domain.services.dispatch_service import DispatchService


class DomainContainer(BaseContainer):
    dispatch_service = providers.Resource(DispatchService)
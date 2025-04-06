from typing import Protocol

from core.domain.shared_kernel.location import Location
from infrastructure.adapters.grpc.out.geo_pb2 import GetGeolocationRequest


class IGeoGrpc(Protocol):
        
    def GetGeolocation(self, request: GetGeolocationRequest) -> Location:
        ...
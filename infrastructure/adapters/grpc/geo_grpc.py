import grpc

from core.domain.shared_kernel.location import Location
from infrastructure.adapters.grpc.out.geo_pb2 import GetGeolocationRequest
from infrastructure.adapters.grpc.out.geo_pb2_grpc import GeoStub


class GeoGrpc:
    def __init__(self, target: str, options: dict | None = None):
        self.__channel = grpc.insecure_channel(target=target, options=options)
        self.stub = GeoStub(self.__channel)
        
    def GetGeolocation(self, request: GetGeolocationRequest) -> Location:
        response = self.stub.GetGeolocation(request)
        return Location(x=response.x, y=response.y)
import asyncio
import grpc
from settings import grpc_settings


async def serve():
    server = grpc.aio.server()
    server.add_insecure_port(grpc_settings.ADDRESS)
    await server.start()
    server.wait_for_termination()
    
    
if __name__ == "__main__":
    asyncio.run(serve())
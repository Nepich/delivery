import granian
from granian.log import LogLevels
from granian.constants import Interfaces


if __name__ == "__main__":
    granian.Granian(
        target="api.adapters.http.contract.src.openapi_server.app:app",
        address="0.0.0.0",
        port=8001,
        interface=Interfaces.ASGI,
        workers=1,
        log_level=LogLevels.info,
        reload=True
    ).serve()
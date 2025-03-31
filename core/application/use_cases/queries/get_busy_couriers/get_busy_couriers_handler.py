from sqlalchemy import text
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_response import GetBusyCouriersResponse, LocationResponse
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_query import GetBusyCouriersQuery
from infrastructure.adapters.postgres.session import async_session
        
        
class GetBusyCouriersHandler:
    async def handle(self, query: GetBusyCouriersQuery) -> list[GetBusyCouriersResponse]:
        async with async_session() as session:
            stmt = text(
                """
                SELECT 
                courier.id id, 
                courier.name name, 
                courier.status status, 
                courier.location_x location_x, 
                courier.location_y location_y, 
                transport.id transport_id
                FROM courier
                LEFT JOIN transport ON courier.id = transport.courier_id
                WHERE status = 'BUSY'
                """
                )
            result = await session.execute(stmt)
            return [
                GetBusyCouriersResponse(
                    id=res["id"],
                    name=res["name"],
                    location=LocationResponse(
                        x=res["location_x"],
                        y=res["location_y"],
                    ),
                    transport_id=res["transport_id"]
                ) for res in result.mappings().all()
            ]
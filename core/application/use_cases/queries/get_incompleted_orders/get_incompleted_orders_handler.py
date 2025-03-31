from sqlalchemy import text
from core.application.use_cases.queries.get_incompleted_orders.get_incompleted_orders_query import GetIncompletedOrdersQuery
from core.application.use_cases.queries.get_incompleted_orders.get_incompleted_orders_response import GetIncompletedOrdersResponse, LocationResponse
from infrastructure.adapters.postgres.session import async_session
        
        
class GetIncompletedOrdersHandler:
    async def handle(self, query: GetIncompletedOrdersQuery) -> list[GetIncompletedOrdersResponse]:
        async with async_session() as session:
            stmt = text(
                """
                SELECT 
                id, 
                status, 
                location_x, 
                location_y
                FROM orders
                WHERE status <> 'COMPLETED'
                """
                )
            result = await session.execute(stmt)
            return [
                GetIncompletedOrdersResponse(
                    id=res["id"],
                    location=LocationResponse(
                        x=res["location_x"],
                        y=res["location_y"],
                    )
                ) for res in result.mappings().all()
            ]
from core.application.use_cases.commands.assigne.assigne_command import AssigneCommand
from core.application.use_cases.commands.assigne.iassigne_handler import IAssigneHandler
from core.application.use_cases.commands.create_order.create_order_command import CreateOrderCommand
from core.application.use_cases.commands.create_order.icreate_order_handler import ICreateOrderHandler
from core.application.use_cases.commands.move_couriers.imove_couriers_handler import IMoveCourierHandler
from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCourierCommand
from core.application.use_cases.queries.get_busy_couriers.iget_busy_couriers_handler import IGetBusyCouriersHandler
from core.application.use_cases.queries.get_busy_couriers.get_busy_couriers_query import GetBusyCouriersQuery
from core.application.use_cases.queries.get_incompleted_orders.get_incompleted_orders_query import GetIncompletedOrdersQuery
from core.application.use_cases.queries.get_incompleted_orders.iget_incompleted_orders_handler import IGetIncompletedOrdersHandler


class Mediator:
    
    def __init__(
        self,
        assign_handler: IAssigneHandler,
        create_order_handler: ICreateOrderHandler,
        move_courier_handler: IMoveCourierHandler,
        get_busy_courier_handler: IGetBusyCouriersHandler,
        get_incompleted_orders_handler: IGetIncompletedOrdersHandler
        ):
        self.__assign_handler = assign_handler
        self.__create_order_handler = create_order_handler
        self.__move_courier_handler = move_courier_handler
        self.__get_busy_courier_handler = get_busy_courier_handler
        self.__get_incompleted_orders_handler = get_incompleted_orders_handler
        
    async def notify(self, command):
        if isinstance(command, MoveCourierCommand):
            return await self.__move_courier_handler.handle(command)
        if isinstance(command, AssigneCommand):
            return await self.__assign_handler.handle(command)
        if isinstance(command, CreateOrderCommand):
            return await self.__create_order_handler.handle(command)
        if isinstance(command, GetBusyCouriersQuery):
            return await self.__get_busy_courier_handler.handle(command)
        if isinstance(command, GetIncompletedOrdersQuery):
            return await self.__get_incompleted_orders_handler.handle(command)
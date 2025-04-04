# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, List
from api.adapters.http.contract.src.openapi_server.models.courier import Courier
from api.adapters.http.contract.src.openapi_server.models.error import Error
from api.adapters.http.contract.src.openapi_server.models.order import Order


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def create_order(
        self,
    ) -> None:
        """Позволяет создать заказ с целью тестирования"""
        ...


    async def get_couriers(
        self,
    ) -> List[Courier]:
        """Позволяет получить всех курьеров"""
        ...


    async def get_orders(
        self,
    ) -> List[Order]:
        """Позволяет получить все незавершенные"""
        ...

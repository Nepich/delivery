from typing import Protocol

from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCourierCommand


class IMoveCourierHandler(Protocol):
    
    async def handle(self, command: MoveCourierCommand):
        ...
from typing import Protocol

from core.application.use_cases.commands.assigne.assigne_command import AssigneCommand


class IAssigneHandler(Protocol):
    
    async def handle(self, command: AssigneCommand):
        ...
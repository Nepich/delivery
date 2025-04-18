from pydantic import BaseModel
from core.primitives.icommand import Command


class AssigneCommand(BaseModel, Command):
    ...
from pydantic import BaseModel

from core.primitives.icommand import Command


class MoveCourierCommand(BaseModel, Command):
    ...
from typing import TypedDict

from pydantic import BaseModel


class Move(BaseModel):
    col: int
    row: int

    def __str__(self) -> str:
        return str(self.model_dump())

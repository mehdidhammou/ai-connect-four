from typing import TypedDict

from pydantic import BaseModel


class Move(BaseModel):
    col: int
    row: int

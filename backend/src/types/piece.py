from typing import Annotated

from pydantic import Field

Piece = Annotated[int, Field(ge=0, le=2)]

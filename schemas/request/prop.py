from typing import Optional

from pydantic import BaseModel


class CreatePropModel(BaseModel):
    name: str
    is_selectable: bool
    options: Optional[list]

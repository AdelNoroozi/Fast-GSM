from typing import Optional

from pydantic import BaseModel


class CreatePropModel(BaseModel):
    prop: str
    is_selectable: bool
    options: Optional[list]

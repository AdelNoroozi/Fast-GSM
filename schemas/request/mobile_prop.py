from typing import Optional

from pydantic import BaseModel


class InputPropModel(BaseModel):
    prop_id: int
    value: str


class CreatePropModel(BaseModel):
    prop: str
    is_selectable: bool
    options: Optional[list]

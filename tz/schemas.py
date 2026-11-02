from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models import Direction


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    full_name: str = Field(min_length=1, max_length=255)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str


class PassEventCreate(BaseModel):
    user_id: int = Field(gt=0)
    direction: Direction


class PassEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    timestamp: datetime
    direction: Direction

from pydantic import BaseModel, Field


class SimGet(BaseModel):
    id: int = Field(..., gt=0)
    number: str = Field(..., min_length=6, max_length=10)
    user: int = Field(..., gt=0)


class SimCreate(BaseModel):
    number: str
    user_id: int

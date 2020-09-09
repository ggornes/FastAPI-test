from typing import List, Optional

from pydantic import BaseModel


class WeightRecordBase(BaseModel):
    weight_kg: float


class WeightRecordCreate(WeightRecordBase):
    pass


class WeightRecord(WeightRecordBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    weight_records: List[WeightRecord] = []

    class Config:
        orm_mode = True
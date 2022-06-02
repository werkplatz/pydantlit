from typing import Union

from pydantic import BaseModel, Field


class Cat(BaseModel):
    meows: int


class Dog(BaseModel):
    barks: float


class Lizard(BaseModel):
    scales: bool


class Model(BaseModel):
    pet: Union[Cat, Dog, Lizard] = Field(...)
    n: int


def __model__():
    return Model(pet=Dog(barks=20), n=1)


__ui_schema__ = {"pet": {"pet_type": {"ui:widget": "hidden"}}}

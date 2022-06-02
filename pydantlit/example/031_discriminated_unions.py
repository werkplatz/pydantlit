from typing import Literal, Union

from pydantic import BaseModel, Field


class Cat(BaseModel):
    pet_type: Literal["cat"]
    meows: int


class Dog(BaseModel):
    pet_type: Literal["dog"]
    barks: float


class Lizard(BaseModel):
    pet_type: Literal["reptile", "lizard"]
    scales: bool


class Model(BaseModel):
    pet: Union[Cat, Dog, Lizard] = Field(..., discriminator="pet_type")
    n: int


def __model__():
    return Model(pet={"pet_type": "dog", "barks": 3.14}, n=1)


__ui_schema__ = {"pet": {"pet_type": {"ui:widget": "hidden"}}}

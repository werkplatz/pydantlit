"""
Recommended way of representing discriminated unions

Discriminated unions are not fully supported by ajv (validator)

"""


from typing import Literal, Union, List, Dict, Any, Type
from pydantic import BaseModel


class Cat(BaseModel):
    meows: int


class Dog(BaseModel):
    barks: float


class Lizard(BaseModel):
    scales: bool


"""
Patching schema to use one field as discriminator and another as value. 
Important: discriminator names are expected to be lowercase of the class names  
"""


def all_of_if_then_schema(
    schema: Dict[str, Any], model: Type, discriminator: str, value: str
):
    all_of = []
    for key in model.__fields__["target"].type_.__args__:
        all_of.append(
            {
                "if": {"properties": {"target": {"const": key}}},
                "then": {
                    "properties": {value: {"$ref": f"#/definitions/{key.capitalize()}"}}
                },
            }
        )
    schema["properties"].pop("value")

    schema["allOf"] = all_of


class Animal(BaseModel):

    target: Literal["cat", "dog", "lizard"] = "cat"
    value: Union[Cat, Dog, Lizard] = None

    class Config:
        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type["Animal"]) -> None:
            all_of_if_then_schema(schema, model, "target", "value")


class Animals(BaseModel):
    __root__: List[Animal]


def __model__():
    return Animals(__root__=[Animal(target="dog", value=Dog(barks=12))])


if __name__ == "__main__":
    print(Animals.schema_json())

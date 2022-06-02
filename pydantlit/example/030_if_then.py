"""
Recommended way of representing multiple choices in a single dictionary

Cannot use discriminated unions are not fully supported by ajv (validator)

"""


from tkinter.messagebox import NO
from typing import Literal, Union, List, Dict, Any, Type
from pydantic import BaseModel


class Cat(BaseModel):
    meows: int


class Dog(BaseModel):
    barks: float


class Lizard(BaseModel):
    scales: bool


"""
Patching schema to enable fields only in the discriminator fiels
"""


def all_of_if_then_schema(schema: Dict[str, Any], model: Type, discriminator):
    all_of = []
    for key in model.__fields__[discriminator].type_.__args__:
        all_of.append(
            {
                "if": {"properties": {discriminator: {"contains": {"const": key}}}},
                "then": {
                    "properties": {key: {"$ref": f"#/definitions/{key.capitalize()}"}}
                },
            }
        )
        schema["properties"].pop(key)

    schema["allOf"] = all_of


class Animals(BaseModel):

    targets: List[Literal["cat", "dog", "lizard"]] = []
    cat: Cat = None
    dog: Dog = None
    lizard: Lizard = None

    class Config:
        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: Type["Animals"]) -> None:
            all_of_if_then_schema(schema, model, "targets")


def __model__():
    return Animals(targets=["dog"], dog=Dog(barks=12))


if __name__ == "__main__":
    print(Animals.schema_json())

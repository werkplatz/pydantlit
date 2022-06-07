"""
from https://pydantic-docs.helpmanual.io/usage/types/#secret-types
"""

from pydantic import BaseModel, SecretStr, SecretBytes

class SimpleModel(BaseModel):
    password: SecretStr
    password_bytes: SecretBytes


__model__ = lambda: SimpleModel(password='IAmSensitive', password_bytes=b'IAmSensitiveBytes')
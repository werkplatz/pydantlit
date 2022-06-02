from pydantic import BaseModel, HttpUrl, PostgresDsn


class UrlModel(BaseModel):
    url: HttpUrl
    postgres: PostgresDsn 


__model__ = lambda: UrlModel(url='http://www.example.com',postgres="postgres://postgres:123456@127.0.0.1:5432/dummy")
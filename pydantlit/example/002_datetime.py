from datetime import date, datetime, time, timedelta
from click import option
from pydantic import BaseModel

try:
    import orjson
except ImportError:
    raise


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(
        v, option=orjson.OPT_SERIALIZE_PYDANTIC | orjson.OPT_UTC_Z, default=default
    ).decode()


class Model(BaseModel):
    d: date = None
    dt: datetime = None
    t: time = None
    # td: timedelta = None # Not supported by orjson

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


def __model__():
    return Model(
        d=1966280412345.6789,
        dt="2032-04-23T10:20:30.400+02:30",
        t=time(4, 8, 16),
        # td='P3DT12H30M5S',
    )

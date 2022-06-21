from json import JSONEncoder
from typing import Any

from .serializable import Serializable


class SerializableEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Serializable):
            return o.to_json()
        return super(SerializableEncoder, self).default(o)

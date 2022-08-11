import json
from json import JSONEncoder
from typing import Any

from event_structure import ValidEventStructureTerm
from serializer import IdRelation, to_relation
from serializer import SerializableEncoder


# with open('es', 'w+') as file:
#     json.dump(rel, file)
#

# with open('es', 'wb+') as file:
#     pickle.dump(es, file)
#
# with open('es', 'rb') as file:
#     esp = pickle.load(file)

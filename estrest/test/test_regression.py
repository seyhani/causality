import json
import os
import unittest

from event_structure import EventStructure
from serializer import to_relation, SerializableEncoder, IdRelation

FILE_PATH = "./test/es.json"


def save_relation(relation: IdRelation):
    encoded = json.dumps(relation, cls=SerializableEncoder)
    with open(FILE_PATH, "w+") as file:
        file.write(encoded)


class TestRegression(unittest.TestCase):

    def test_regression(self):
        es = EventStructure().prefix('b').prefix('a').plus(EventStructure().prefix('y').prefix('x'))
        relation = to_relation(es)

        if os.getenv('SAVE_REL') == 'true':
            save_relation(relation)

        with open(FILE_PATH, "r") as file:
            deserialized = file.read()
        decoded_relation = IdRelation.from_json(json.loads(deserialized))
        self.assertEqual(relation, decoded_relation)


if __name__ == '__main__':
    unittest.main()

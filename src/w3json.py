import json
from json import JSONEncoder


class StructEncoder(JSONEncoder):
        def default(self, o):
            try:
                return o.as_dict()
            except:
                return str(o)

class w3json(object):

    @staticmethod
    def dumps(obj):
        return json.dumps(obj,cls=StructEncoder)

    @staticmethod
    def loads(obj):
        return json.loads(obj)

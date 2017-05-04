import decimal
from flask.json import JSONEncoder


class CustomDecimalJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, decimal.Decimal):
                # wanted a simple yield str(o) in the next line,
                # but that would mean a yield on the line with super(...),
                # which wouldn't work (see my comment below), so...
                return (str(o) for o in [obj])
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
from bson.objectid import ObjectId
from datetime import datetime


def to_json_safe(doc: dict) -> dict:
    out = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        elif isinstance(v, datetime):
            out[k] = v.isoformat()
        elif isinstance(v, bytes):
            continue
        else:
            out[k] = v
    return out

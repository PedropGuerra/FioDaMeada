import json


def dict_to_json(objeto: dict) -> str:
    return json.dumps(objeto)


def json_to_dict(objeto: str) -> dict:
    return json.loads(objeto)

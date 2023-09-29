import json

def read_noticias(path):
    with open(path, "r") as txt:
        return json.loads(txt.read())
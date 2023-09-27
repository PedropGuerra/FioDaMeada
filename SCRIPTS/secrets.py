import os

with open("env_variables.txt", "r") as txt:
    global txt_dict
    txt = list(map(lambda index: index.replace("\n", "").split(":"), txt.readlines()))
    txt_dict = {index[0]: index[1] for index in txt}


def getenv(key):
    try:
        return txt_dict[key]

    except:
        return None


def setenv(key, value) -> None:
    # os.environ[f"{key}"] = value
    txt_dict[key] = value
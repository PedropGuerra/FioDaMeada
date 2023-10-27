with open("env_variables.txt", "r") as txt:
    global txt_dict
    txt = list(map(lambda index: index.replace("\n", "").split(":"), txt.readlines()))
    txt_dict = {index[0]: index[1] for index in txt}


def getenv(key, default=None):
    return txt_dict[key] if key in txt_dict else default


def setenv(key, value) -> None:
    # os.environ[f"{key}"] = value
    txt_dict[key] = value

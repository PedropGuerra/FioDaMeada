with open("env_variables.txt", "r") as txt:
    global txt_dict
    txt = list(map(lambda index: index.replace("\n", "").split(":"), txt.readlines()))
    txt_dict = {index[0]: index[1] for index in txt}


def getenv(key):
    return txt_dict[key]

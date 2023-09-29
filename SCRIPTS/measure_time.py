from time import time

global measure_time_dict
measure_time_dict = {
    "middle" : {
        'result' : 0},
}

def measure_time(identifier: str, stage: str):
    start = time()
    match stage:
        case "init":
            measure_time_dict[identifier] = {}
            measure_time_dict[identifier]["init"] = time()
        
        case "end":
            measure_time_dict[identifier]["end"] = time()
            measure_time_dict[identifier]["result"] = measure_time_dict[identifier]["end"] - measure_time_dict[identifier]["init"]
    
    measure_time_dict["middle"]["result"] += time() - start


def show_measure() -> dict:
    return measure_time_dict
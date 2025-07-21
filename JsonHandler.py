import json

json_file_name = "nodesHistory.json"


def __save_to_json_given_file_name(file_name, dict_list):
    with open(file_name, 'w') as file:
        json.dump(dict_list, file)


def __load_from_json_given_file_name(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data
    except:
        print("No previous records available.")


def save_to_json(dict_list):
    __save_to_json_given_file_name(json_file_name, dict_list)


def load_from_json():
    loaded_json_file = __load_from_json_given_file_name(json_file_name)
    if loaded_json_file is None:
        loaded_json_file = []
    return loaded_json_file

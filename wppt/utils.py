"""A sample module."""

import yaml


def parse_definitions(directory):
    definitions = {}
    for file in walk_dir(directory, ".yaml"):
        definitions.update(read_yaml(file))
    return definitions


def walk_dir(directory, file_extension):
    import os

    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                file_list.append(os.path.join(root, file))
    return file_list


def read_yaml(file_path):
    yaml_definitions = None
    with open(file_path, "r") as file:
        yaml_definitions = yaml.load(file, Loader=yaml.FullLoader)

    return yaml_definitions


def traverse_format_dict(dictionary, data):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            traverse_format_dict(value, data)
        else:
            try:
                dictionary[key] = value.format(data=data)
            except KeyError as ಠ_ಠ:
                raise KeyError(f"Key {ಠ_ಠ} not found in data")

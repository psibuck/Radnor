"""Contains helper functions to assist with the processing of json data."""

import os
import json
from datetime import date

def __get_json_data(file):
    if os.path.exists(file):
        with open(file, encoding='UTF-8') as json_file:
            # if file is empty this is an exception
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return None

def load_object_from_json(file, object_to_load):
    """Loads the given object from the given file."""
    data = __get_json_data(file)
    if data is not None:
        if hasattr(object_to_load, "from_json"):
            object_to_load.from_json(data)
        else:
            print("ERROR: failed to load object as from_json not implemented")

def save_object_to_json(file: str, object):
    """Writes the given object to the given file."""
    with open(file, 'w', encoding='UTF-8') as json_file:
        as_json = json.dumps(object.to_json(), indent = 4)
        json_file.write(as_json)

def load_from_json(file, content_class, array):
    """Extracts json data from the given file and attempts to load it into an object."""
    data = __get_json_data(file)
    if data is not None:
        for entry in data:
            new_object = content_class()
            if hasattr(new_object, "from_json"):
                new_object.from_json(entry)
                array.append(new_object)
            else:
                print("ERROR: failed to load object as from_json not implemented")

def save_to_json(file: str, objects):
    """Saves the given objects to the given file."""
    with open(file, 'w', encoding='UTF-8') as json_file:
        data = []
        for gen_object in objects:
            data.append(gen_object.to_json())
        json_blob = json.dumps(data, indent = 4)
        json_file.write(json_blob)

def json_get(blob, variable_name, class_name=None, type =str):
    """Attempts to retrieve an object from a blob of data."""
    try:
        variable = blob[variable_name]
        if class_name is not None:
            return class_name(variable)
        elif type is not None:
            if type == date:
                return date.fromisoformat(variable)
        return variable
    except KeyError:
        if class_name is not None:
            return None

        if type == int:
            return 0
        elif type == float:
            return 0.0
        elif type == date:
            return date.today()
        return ""
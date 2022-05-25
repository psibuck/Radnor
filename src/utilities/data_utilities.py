import os, json

def __GetJsonData(file):
    if os.path.exists(file):
        with open(file) as json_file:
            # if file is empty this is an exception
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                return None

def LoadObjectFromJson(file, object):
    data = __GetJsonData(file)
    if data is not None:
        if hasattr(object, "FromJson"):
            object.FromJson(data)
        else:
            print("ERROR: failed to load object as FromJson not implemented")

def SaveObjectToJson(file, object):
    with open(file, 'w') as json_file:
        as_json = json.dumps(object.ToJson(), indent = 4)
        json_file.write(as_json)

def LoadFromJson(file, content_class, array):
    data = __GetJsonData(file)
    if data is not None:
        for entry in data:
            new_object = content_class()
            if hasattr(new_object, "FromJson"):
                new_object.FromJson(entry)
                array.append(new_object)
            else:
                print("ERROR: failed to load object as FromJson not implemented")

def SaveToJson(file, objects):
    with open(file, 'w') as json_file:
        data = []
        for object in objects:
            data.append(object.ToJson())
        json_blob = json.dumps(data, indent = 4)
        json_file.write(json_blob)

def JsonGet(blob, variable_name, class_name=None, type=str):
    try:
        variable = blob[variable_name]
        if class_name is not None:
            return class_name(variable)
        else:
            return variable
    except KeyError:
        if class_name is not None:
            return None

        if type == int:
            return 0
        elif type == float:
            return 0.0
        return ""

def GetDateString(raw_data):
    if len(raw_data) != 6:
        print("ERROR: date incorrectly formatted")
    return raw_data[:2] + "/" + raw_data[2:4] + "/20" + raw_data[4:]
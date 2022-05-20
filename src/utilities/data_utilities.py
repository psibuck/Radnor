import os, json

def LoadFromJson(file, content_class, array):
    if os.path.exists(file):
        with open(file) as json_file:
            # if file is empty this is an exception
            try:
                data = json.load(json_file)
                for entry in data:
                    new_object = content_class()
                    if hasattr(new_object, "FromJson"):
                        new_object.FromJson(entry)
                        array.append(new_object)
                    else:
                        print("ERROR: failed to load object as FromJson not implemented")
            except json.JSONDecodeError:
                pass

def SaveToJson(file, objects):
    with open(file, 'w') as json_file:
        data = []
        for object in objects:
            data.append(object.ToJson())
        json_blob = json.dumps(data, indent = 4)
        json_file.write(json_blob)


def SaveObjects(file_name, object_list):
    file_to_write = open(file_name, 'w+')

    for object in object_list:
        object.Save(file_to_write)

def ProcessData(raw_data):
    raw_data = raw_data.strip("\n").split(",")
    return raw_data
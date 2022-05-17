

def SaveObjects(file_name, object_list):
    file_to_write = open(file_name, 'w')

    for object in object_list:
        object.Save(file_to_write)

def ProcessData(raw_data):
    raw_data = raw_data.strip("\n").split(",")
    return raw_data

def GenerateListString(list):
    string_out = "["
    initial = True
    for entry in list:
        if not initial:
            string_out += ","
        else:
            initial = False
        
        string_out += str(entry)
    string_out += "]"
    return string_out

def LoadArray(data):
    data = data.strip("[").strip("]")
    return data.split(",")
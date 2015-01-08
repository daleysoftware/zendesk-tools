import json

def merge_json_objects(label1, o1, label2, o2):
    data = {label1: o1, label2: o2}
    return json.loads(json.dumps(data))
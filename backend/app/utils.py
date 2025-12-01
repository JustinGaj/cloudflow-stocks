import os
import json

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def write_json(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f, indent=2)
"""
Author:  Josh Fogus
Description:  A series of utility functions for writing output to files. 
"""

import json
from utilities.exceptions import InputException


def write_json(file_path, json_obj):
    try:
        with open(file_path, 'w') as file:
            json.dump(json_obj, file, indent=4)
    except IOError as exc:
        raise InputException from exc
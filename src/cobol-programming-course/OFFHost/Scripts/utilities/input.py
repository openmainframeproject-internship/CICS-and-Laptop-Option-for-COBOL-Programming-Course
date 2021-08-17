"""
Author:  Josh Fogus
Description:  A series of utility functions for reading input. 
"""

import json
from utilities.exceptions import InputException


def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            input_json = json.load(file)
    except IOError as exc:
        raise InputException from exc

    return input_json


def read_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            input_txt = file.read()
    except IOError as exc:
        raise InputException from exc

    return input_txt

"""
Author:  Josh Fogus
Description:  Exceptions to be used in the cobol course.
"""

from os import error


class Error(Exception):
    pass


class ESCWAException(Error):
    pass


class InputException(Error):
    pass


class HTTPException(Error):
    pass
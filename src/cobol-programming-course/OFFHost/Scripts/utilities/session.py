"""
Author:  Josh Fogus
Description:  Functions for handling sessions and cookies. 
"""

import os
import pickle
import requests


def read_cookies():
    """ Reads in a previously pickled cookies file. """

    cookies_path = os.path.join(os.getcwd(), 'session/cookies')

    try:
        with open(cookies_path, 'rb') as cookies_file:
            cookies = pickle.load(cookies_file)
    except IOError as exc:
        return None

    return cookies


def get_session():
    """ Creates a session with cookies if available. """

    session = requests.Session()
    cookies = read_cookies()

    if cookies:
        session.cookies.update(cookies)

    return session


def save_cookies(cookies):
    """ Saves session cookies to a path. """

    cookies_path = os.path.join(os.getcwd(), 'session/cookies')

    try:
        with open(cookies_path, 'wb') as cookies_file:
            pickle.dump(cookies, cookies_file)
    except IOError as exc:
        return
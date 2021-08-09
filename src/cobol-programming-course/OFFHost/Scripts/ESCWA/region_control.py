"""
Author:  Josh Fogus
Description:  Functions for control of a Micro Focus server region. 
"""

import time
import requests
from utilities.session import get_session, save_cookies
from utilities.misc import create_headers, check_http_error
from utilities.input import read_json
from utilities.exceptions import ESCWAException, InputException, HTTPException


def add_region(region_name, ip_address, port, template_file):
    """ Adds a region to the Micro Focus server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86'.format(ip_address, ip_address)
    req_headers = create_headers('CreateRegion', ip_address)

    try:
        req_body = read_json(template_file)
    except InputException as exc:
        raise ESCWAException('Unable to read template file: {}.'.format(template_file)) from exc
    
    req_body['CN'] = region_name
    req_body['mfTN3270ListenerPort'] = port
    session = get_session()

    try:
        res = session.post(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Add Region API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Add Region API request.') from exc

    save_cookies(session.cookies)

    return res


def start_region(region_name, ip_address):
    """ Starts a previously created region on the Micro Focus server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}/start'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)
    req_body = {
        'mfUser': 'SYSAD',
        'mfPassword': 'SYSAD',
        'mfUseSession': 'true',
        'mfColdStart': 'true'
    }

    session = get_session()

    try:
        res = session.post(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Start Region API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Start Region API request.') from exc

    save_cookies(session.cookies)

    return res


def stop_region(region_name, ip_address):
    """ Stops a previously created region on the Micro Focus server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}/stop'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)
    req_body = {
        'mfUser': 'SYSAD',
        'mfPassword': 'SYSAD',
        'mfUseSession': 'true',
        'mfClearDynamic': 'true',
        'mfForceStop': 'true'
    }

    session = get_session()

    try:
        res = session.post(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Stop Region API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Stop Region API request.') from exc

    save_cookies(session.cookies)

    return res


def mark_region_stopped(region_name, ip_address):
    """ Marks a previously created region as stopped on the Micro Focus server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)
    req_body = {
        'mfServerStatus': 'Stopped'
    }

    session = get_session()

    try:
        res = session.put(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Mark Region Stopped API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Mark Region Stopped API request.') from exc

    save_cookies(session.cookies)

    return res


def del_region(region_name, ip_address):
    """ Deletes a region from the Micro Focus server. """
    
    uri = 'http://{}:10086/native/v1/regions/{}/86/{}'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)
    session = get_session()

    try:
        res = session.delete(uri, headers=req_headers)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Delete Region API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Delete Region API request.') from exc

    save_cookies(session.cookies)

    return res


def get_region_status(region_name, ip_address):
    """ Checks a previously created region's status on the Micro Focus Server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}/status'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)

    session = get_session()

    try:
        res = session.get(uri, headers=req_headers)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Region Check API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Region Check API request.') from exc

    save_cookies(session.cookies)
    
    return res


def confirm_region_status(region_name, ip_address, mins_allowed, expected):
    """ Checks a previously created region's status for a given value on the Micro Focus Server. """

    while mins_allowed >= 0:
        status_res = get_region_status(region_name, ip_address)
        status_res = status_res.json()

        if status_res['mfServerStatus'] == expected:
            return True

        if mins_allowed != 0:
            time.sleep(60)

        mins_allowed -= 1
    
    return False
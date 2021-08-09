"""
Author:  Josh Fogus
Description:  Functions for configuration of MFDS lists on the Micro Focus server.
"""

import requests
from utilities.misc import create_headers, check_http_error
from utilities.session import get_session, save_cookies
from utilities.exceptions import ESCWAException, HTTPException


def check_mfds_list(ip_address):
    """ Check the MFDS list of a Micro Focus server. """

    uri = 'http://{}:10086/server/v1/config/mfds'.format(ip_address)
    req_headers = create_headers('CreateRegion', ip_address)
    session = get_session()

    try:
        res = session.post(uri, headers=req_headers)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Check MFDS API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Check MFDS API request.') from exc

    save_cookies(session.cookies)

    return res


def add_mfds_to_list(ip_address, mfds_description):
    """ Add an MFDS to a Micro Focus server. """

    uri = 'http://{}:10086/server/v1/config/mfds'.format(ip_address)
    req_headers = create_headers('CreateRegion', ip_address)
    req_body = {
        'MfdsHost': ip_address,
        'MfdsPort': 86,
        'MfdsIdentifier': 'CI60Test',
        'MfdsDescription': mfds_description
    }

    session = get_session()

    try:
        res = session.post(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Add MFDS API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Add MFDS API request.') from exc

    save_cookies(session.cookies)

    return res
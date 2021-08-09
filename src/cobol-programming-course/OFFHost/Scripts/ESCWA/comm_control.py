"""
Author:  Josh Fogus
Description:  A function to setup a JES listener on the Micro Focus server. 
"""

import requests
from utilities.misc import get_elem_with_prop, create_headers, check_http_error
from utilities.session import get_session, save_cookies
from utilities.exceptions import ESCWAException, HTTPException


def set_jes_listener(region_name, ip_address, port):
    """ Sets a JES listener on the Micro Focus server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}/commsserver'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)
    session = get_session()

    try:
        res = session.get(uri, headers=req_headers)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to get Comm Server information.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to get Comm Server information.') from exc

    comm_server = res.json()
    uri += '/{}/listener'.format(comm_server[0]['mfServerUID'])

    try:
        res = session.get(uri, headers=req_headers)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to get Comm Server Listener information.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to get Comm Server Listener information.') from exc

    listener_list = res.json()
    req_body = {'mfRequestedEndpoint': 'tcp:127.0.0.1:{}'.format(port)}
    listener = get_elem_with_prop(listener_list, 'CN', 'Web Services and J2EE')
    uri += '/{}'.format(listener['mfUID'])
    
    try:
        res = session.put(uri, headers=req_headers, json=req_body)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to update Web Services and J2EE Listener.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to update Web Services and J2EE Listener.') from exc

    save_cookies(session.cookies)
    
    return res
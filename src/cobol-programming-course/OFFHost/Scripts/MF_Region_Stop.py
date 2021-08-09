#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to stop a Micro Focus Server. 
"""

import sys
from utilities.misc import parse_args
from ESCWA.region_control import stop_region
from ESCWA.region_control import confirm_region_status
from utilities.exceptions import ESCWAException


def stop_server(region_name='OMPTRAIN', ip_address='127.0.0.1', mins_allowed=1):
    try:
        stop_res = stop_region(region_name, ip_address)
    except ESCWAException as exc:
        print('Unable to stop region.')
        sys.exit(1)

    try:
        confirmed = confirm_region_status(region_name, ip_address, mins_allowed, 'Stopped')
    except ESCWAException as exc:
        print('Unable to check region.')
        sys.exit(1)
    
    if not confirmed:
        print('Micro Focus JES Batch Server has failed to stop')
        sys.exit(1)

    print('Micro Focus JES Batch Server has stopped successfully')


if __name__ == '__main__':
    short_map = {}
    long_map = {
        '--RegionName': 'region_name',
        '--MFDSIPAddress': 'ip_address',
        '--MinsAllowed': 'mins_allowed'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    stop_server(**kwargs)
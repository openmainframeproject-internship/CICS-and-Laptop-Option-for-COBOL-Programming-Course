#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to reset a Micro Focus server region to stopped. 
"""

import sys
from ESCWA.region_control import mark_region_stopped, confirm_region_status
from utilities.misc import parse_args
from utilities.exceptions import ESCWAException


def reset_region(region_name='OMPTRAIN', ip_address='127.0.0.1', mins_allowed=1):
    try:
        mark_res = mark_region_stopped(region_name, ip_address)
    except ESCWAException as exc:
        print('Unable to mark region as stopped.')
        sys.exit(1)

    try:
        confirmed = confirm_region_status(region_name, ip_address, mins_allowed, 'Stopped')
    except ESCWAException as exc:
        print('Unable to confirm region is stopped.')
        sys.exit(1)

    if not confirmed:
        print('Unable to confirm region is stopped.')
        sys.exit(1)

    print('Micro Focus JES Batch Server has been successfully set to Stopped')       


if __name__ == '__main__':
    short_map = {}
    long_map = {
        '--RegionName': 'region_name',
        '--MFDSIPAddress': 'ip_address',
        '--MinsAllowed': 'mins_allowed'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    reset_region(**kwargs)
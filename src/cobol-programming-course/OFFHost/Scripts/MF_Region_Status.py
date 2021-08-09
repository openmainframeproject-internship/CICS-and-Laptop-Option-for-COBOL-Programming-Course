#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script for checking the status of a Micro Focus Server region. """

import sys
from utilities.misc import parse_args
from ESCWA.region_control import get_region_status
from utilities.exceptions import ESCWAException


def check_status(region_name='OMPTRAIN', ip_address='127.0.0.1'):
    try:
        status_res = get_region_status(region_name, ip_address)
    except ESCWAException as exc:
        print('Unable to check region.')
        sys.exit(1)

    status_res = status_res.json()

    print('Current Status of the Micro Focus JES Batch Server is {}'.format(status_res['mfServerStatus']))


if __name__ == '__main__':
    short_map = {}
    long_map = {
        '--RegionName': 'region_name',
        '--MFDSIPAddress': 'ip_address',
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    check_status(**kwargs)
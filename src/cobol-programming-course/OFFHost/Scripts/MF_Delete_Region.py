#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to delete a Micro Focus server region. 
"""

import sys
from utilities.misc import parse_args
from ESCWA.region_control import confirm_region_status, del_region
from utilities.exceptions import ESCWAException


def delete_server(region_name='OMPTRAIN', ip_address='127.0.0.1'):
    """ Deletes a Micro Focus server. """
    
    try:
        confirmed = confirm_region_status(region_name, ip_address, 0, 'Stopped')
    except ESCWAException as exc:
        # TODO: This triggers when the region is deleted successfully.
        print('Unable to check region status.')
        sys.exit(1)

    if not confirmed:
        print('Region is not stopped; Please stop the region before deleting.')
        sys.exit(1)

    try:
        del_res = del_region(region_name, ip_address)
    except ESCWAException as exc:
        print('Unable to delete region.')
        sys.exit(1)

    if del_res.status_code != 204:
        print('Unable to delete environment at this time')
        sys.exit(1)
    
    print('Environment deleted successfully')


if __name__ == '__main__':
    short_map = {}
    long_map = {
        '--RegionName': 'region_name',
        '--MFDSIPAddress': 'ip_address'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    delete_server(**kwargs)
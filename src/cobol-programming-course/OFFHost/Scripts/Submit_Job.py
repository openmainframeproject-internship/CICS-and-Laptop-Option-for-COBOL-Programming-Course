#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to submit a JCL job to the Micro Focus JES server region.
"""

import sys
from utilities.misc import parse_args
from ESCWA.job_control import submit_jcl, check_job
from utilities.exceptions import ESCWAException


def submit_job(jcl_file, working_folder, ip_address='127.0.0.1', region_name='OMPTRAIN'):
    try:
        submit_res = submit_jcl(region_name, ip_address, jcl_file)
    except ESCWAException as exc:
        print('Unable to submit job.')
        sys.exit(1)

    submit_res = submit_res.json()
    job_id = submit_res['JobMsg'][0].split()[1]

    print('', submit_res['JobMsg'][0], submit_res['JobMsg'][1], sep='\n')

    try:
        run_res = check_job(region_name, ip_address, job_id)
    except ESCWAException as exc:
        print('Unable to check job.')
        sys.exit(1)

    run_res = run_res.json()

    print('', run_res['SysoutMsgs'][0], run_res['SysoutMsgs'][1])


if __name__ == '__main__':
    # Use : after short_map keys and = after long_map keys to indicate required arguments as in getopt
    short_map = {}
    long_map = {
        '--RegionName': 'region_name',
        '--RegionHost': 'ip_address',
        '--JCLFileName=': 'jcl_file',
        '--WSpaceFolder=': 'working_folder'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    submit_job(**kwargs)
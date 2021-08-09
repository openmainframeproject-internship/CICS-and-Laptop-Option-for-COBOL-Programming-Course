#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to get the output from a job previously submitted to the Micro Focus JES server.
"""

import sys
import os
from utilities.misc import parse_args
from ESCWA.job_control import check_job, get_output
from utilities.exceptions import ESCWAException


def get_job_output(job_id, working_folder, ip_address='127.0.0.1', region_name='OMPTRAIN'):
    try:
        check_res = check_job(region_name, ip_address, job_id)
    except ESCWAException as exc:
        print('Unable to check job status.')
        sys.exit(1)

    check_res = check_res.json()
    out_dir = os.path.join(working_folder, 'Output')

    print('', check_res['SysoutMsgs'][0], check_res['SysoutMsgs'][1], sep='\n')

    if check_res['JobStatus'] != 'Complete ':
        print('Job is not yet complete.')
        sys.exit(1)

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    for spool_out in check_res['JobDDs']:
        try:
            out_res = get_output(region_name, ip_address, spool_out['DDEntityName'], spool_out['DDCode'])
        except ESCWAException as exc:
            print('Unable to get job output.')
            sys.exit(1)

        out_res = out_res.json()

        out_filename = '{}_{}_{}.txt'.format(check_res['JobName'], job_id, spool_out['DDName'])
        out_path = os.path.join(out_dir, out_filename)
        line_count = int(spool_out['DDRecords'])

        try:
            with open(out_path, 'w') as file:
                for i in range(line_count):
                    file.write(out_res['Messages'][i] + '\n')
        except IOError as exc:
            print('Unable to write output to file.')
            sys.exit(1)


if __name__ == "__main__":
    short_map = {}
    long_map = {
        '--RegionName': 'region_name',
        '--RegionHost': 'ip_address',
        '--JobID=': 'job_id',
        '--WSpaceFolder=': 'working_folder'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    get_job_output(**kwargs)
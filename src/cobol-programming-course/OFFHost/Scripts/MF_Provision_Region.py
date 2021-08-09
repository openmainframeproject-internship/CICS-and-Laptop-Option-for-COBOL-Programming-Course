#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to create a Micro Focus server region. 
"""

import os
import sys
from utilities.misc import parse_args
from ESCWA.mfds_config import add_mfds_to_list, check_mfds_list
from ESCWA.region_control import add_region, start_region, del_region, confirm_region_status
from ESCWA.region_config import update_region, update_alias, add_initiator, add_datasets
from ESCWA.comm_control import set_jes_listener
from utilities.exceptions import ESCWAException


def create_region(working_dir, sys_base, ip_address='127.0.0.1', region_name='OMPTRAIN', base_config='base.json',
        env_file='./NewRegion_Environment.txt', update_config='update.json', alias_config='alias.json', 
        init_config='init.json', data_dir='datasets'):

    region_port = 9023
    jes_port = 9001

    cwd = os.getcwd()
    config_dir = os.path.join(cwd, 'config')
    dataset_dir = os.path.join(cwd, data_dir)

    base_config = os.path.join(config_dir, base_config)
    update_config = os.path.join(config_dir, update_config)
    alias_config = os.path.join(config_dir, alias_config)
    init_config = os.path.join(config_dir, init_config)

    datafile_list = [file for file in os.scandir(dataset_dir)]

    if ip_address != '127.0.0.1':
        try:
            mfds_list = check_mfds_list(ip_address)
        except ESCWAException as exc:
            print('Unable to check MFDS list.')
            sys.exit(1)

        mfds_list = mfds_list.json()
        mfds_set = False

        for host_id in mfds_list['MfdsHost']:
            if host_id == ip_address:
                mfds_set = True

        if mfds_set is False:
            try:
                add_mfds_to_list(ip_address, 'New Remote MFDS')
            except ESCWAException as exc:
                print('Unable to add MFDS to list.')
                sys.exit(1)

    try:
        add_region(region_name, ip_address, region_port, base_config)
    except ESCWAException as exc:
        print('Unable to create region.')
        sys.exit(1)

    try:
        update_region(region_name, ip_address, update_config, env_file, 'Test Region', sys_base)
    except ESCWAException as exc:
        print('Unable to update region.')
        sys.exit(1)

    try:
        set_jes_listener(region_name, ip_address, jes_port)
    except ESCWAException as exc:
        print('Unable to set JES listener.')
        sys.exit(1)

    try:
        start_region(region_name, ip_address)
    except ESCWAException as exc:
        print('Unable to start region.')
        sys.exit(1)

    try:
        confirmed = confirm_region_status(region_name, ip_address, 1, 'Started')
    except ESCWAException as exc:
        print('Unable to check region status.')
        sys.exit(1)

    if not confirmed:
        print('Region Failed to start. Environment being rewound')

        del_res = del_region(region_name, ip_address)

        if del_res.status_code == 204:
            print('Environment cleaned successfully')
        
        sys.exit(1)
    
    try:
        update_alias(region_name, ip_address, alias_config)
    except ESCWAException as exc:
        print('Unable to update aliases.')
        sys.exit(1)

    try:
        add_initiator(region_name, ip_address, init_config)
    except ESCWAException as exc:
        print('Unable to add initiator.')
        sys.exit(1)

    try:
        add_datasets(region_name, ip_address, working_dir, datafile_list)
    except ESCWAException as exc:
        print('Unable to add datasets.')
        sys.exit(1)


if __name__ == '__main__':
    short_map = {}
    long_map = {
        '--WorkspaceFolder=': 'working_dir',
        '--SystemBase=': 'sys_base',
        '--RegionHost': 'ip_address',
        '--RegionName': 'region_name',
        '--BaseConfig': 'base_config',
        '--ESEnvironmentFile': 'env_file',
        '--UpdateConfig': 'update_config',
        '--AliasConfig': 'alias_config',
        '--InitiatorConfig': 'init_config',
        '--DataConfig': 'data_dir'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    create_region(**kwargs)
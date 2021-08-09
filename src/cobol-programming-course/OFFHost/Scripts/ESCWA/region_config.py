"""
Author:  Josh Fogus
Description:  Function for configuring a Micro Focus server region. 
"""

import os
import sys
import requests
from utilities.misc import create_headers, check_http_error
from utilities.input import read_json, read_txt
from utilities.session import get_session, save_cookies
from utilities.exceptions import ESCWAException, InputException, HTTPException


def update_region(region_name, ip_address, template_file, env_file, region_description, region_base):
    """ Updates the settings of a previously created region on the Micro Focus server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)

    if sys.platform.startswith('win32'):
        path_sep = ';'
    else:
        path_sep = ':'

    esp_alias = '$ESP'
    log_dir = os.path.join(esp_alias, 'Logs')
    loadlib_dir = os.path.join(esp_alias, 'Loadlib')
    sysloadlib_dir = os.path.join(esp_alias, 'SysLoadlib')
    catalog_dir = os.path.join(esp_alias, 'Catalog')
    catalog_data_dir = os.path.join(catalog_dir, 'Data')
    data_dir = os.path.join(esp_alias, 'Data')
    rdef_dir = os.path.join(esp_alias, 'RDEF')

    catalog_file = os.path.join(catalog_dir, 'CATALOG.DAT')
    lib_path = loadlib_dir + path_sep + sysloadlib_dir

    try:
        req_body = read_json(template_file)
    except InputException as exc:
        raise ESCWAException('Unable to read template file: {}.'.format(template_file)) from exc

    try:
        req_body['mfConfig'] = read_txt(env_file)
    except InputException as exc:
        raise ESCWAException('Unable to read env file: {}.'.format(env_file)) from exc

    req_body['CN'] = region_name
    req_body['mfConfig'] = req_body['mfConfig'].replace('##RegionBase', region_base)
    req_body['description'] = region_description
    req_body['mfCASSysDir'] = log_dir
    req_body['mfCASTXTRANP'] = lib_path
    req_body['mfCASTXFILEP'] = catalog_data_dir
    req_body['mfCASTXMAPP'] = lib_path
    req_body['mfCASTXRDTP'] = rdef_dir
    req_body['mfCASJCLPATH'] = lib_path
    req_body['mfCASMFSYSCAT'] = catalog_file
    req_body['mfCASJCLALLOCLOC'] = data_dir

    print(req_body)

    session = get_session()

    try:
        res = session.put(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Update Region API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Update Region API request.') from exc

    save_cookies(session.cookies)

    return res


def update_alias(region_name, ip_address, alias_file):
    """ Updates the aliases on a Micro Focus Server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}/alias'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)

    try:
        req_body = read_json(alias_file)
    except InputException as exc:
        raise ESCWAException('Unable to read alias file: {}'.format(alias_file)) from exc

    session = get_session()

    try:
        res = session.post(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Update Alias API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Update Alias API request.') from exc

    save_cookies(session.cookies)

    return res


def add_initiator(region_name, ip_address, template_file):
    """ Adds an initiator to a Micro Focus server. """

    uri = 'http://{}:10086/native/v1/regions/{}/86/{}/initiator'.format(ip_address, ip_address, region_name)
    req_headers = create_headers('CreateRegion', ip_address)

    try:
        req_body = read_json(template_file)
    except InputException as exc:
        raise ESCWAException('Unable to read initiator file: {}'.format(template_file))

    req_body['CN'] = region_name
    session = get_session()

    try:
        res = session.post(uri, headers=req_headers, json=req_body)
        check_http_error(res)
    except requests.exceptions.RequestException as exc:
        raise ESCWAException('Unable to complete Add Initiator API request.') from exc
    except HTTPException as exc:
        raise ESCWAException('Unable to complete Add Initiator API request.') from exc

    save_cookies(session.cookies)

    return res


def add_datasets(region_name, ip_address, working_dir, datafile_list):
    """ Adds data sets to a Micro Focus server. """

    req_headers = create_headers('CreateRegion', ip_address)
    labs_dir = os.path.join(working_dir, 'COBOL Programming Course #1 - Getting Started', 'Labs')
    jclproc_dir = os.path.join(labs_dir, 'jclproc')
    user_data_file = os.path.join(labs_dir, 'data', 'data')

    try:
        dataset_list = [read_json(data_file) for data_file in datafile_list]
    except InputException as exc:
        raise ESCWAException('Unable to read dataset files')

    responses = []
    session = get_session()

    for dataset in dataset_list:
        uri = 'http://{}:10086/native/v1/regions/{}/86/{}/catalog/{}'.format(ip_address, ip_address, region_name, dataset['jDSN'])

        if dataset['jDSN'] == 'SYS1.PROCLIB':
            dataset['jPCN'] = jclproc_dir
        elif dataset['jDSN'] == 'MFUSER.DATA':
            dataset['jPCN'] = user_data_file

        try:
            res = session.post(uri, headers=req_headers, json=dataset)
            check_http_error(res)
        except requests.exceptions.RequestException as exc:
            raise ESCWAException('Unable to complete Add Dataset API request.') from exc
        except HTTPException as exc:
            raise ESCWAException('Unable to complete Add Dataset API request.') from exc

        responses.append(res)

    save_cookies(session.cookies)

    return responses
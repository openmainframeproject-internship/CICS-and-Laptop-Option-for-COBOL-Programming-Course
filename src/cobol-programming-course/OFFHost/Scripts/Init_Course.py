#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to initialize files based on the local system.
"""

import os
import sys
from shutil import copy2
from xml.etree import ElementTree
from utilities.input import read_json
from utilities.output import write_json
from utilities.misc import parse_args, get_elem_with_prop


def init_course(working_dir):
    """ Creates files in the coursework respective of the local system. """

    ##################
    # Create build.xml
    ##################
    load_dir = os.path.join(working_dir, 'OFFHost', 'System', 'Loadlib')
    script_dir = os.path.join(working_dir, 'OFFHost', 'Scripts')

    build_file_name = 'build.xml'
    template_file = os.path.join(working_dir, 'OFFHost', 'Templates', build_file_name)
    build_file = os.path.join(script_dir, build_file_name)
    
    copy2(template_file, build_file)

    try:
        build_xml_tree = ElementTree.parse(build_file)
    except ElementTree.ParseError as exc:
        print('Unable to read build file: {}'.format(build_file_name))
        sys.exit(1)

    build_xml_root = build_xml_tree.getroot()
    build_xml_root.set('basedir', working_dir)

    for prop in build_xml_root.findall('property'):
        if prop.get('name') == 'loaddir':
            prop.set('value', load_dir)

    build_xml_tree.write(build_file)

    ##################
    # Update env variables in tasks.json
    ##################
    if sys.platform.startswith('win32'):
        # Works for EDBT, if MFED change to Enterprise Develoepr in java_home and mfant
        ant_home = 'C:\\Program Files (x86)\\Ant\\apache-ant-1.10.11'
        java_home = 'C:\\Program Files (x86)\\Micro Focus\\Enterprise Developer Build Tools\\AdoptOpenJDK\\jre'
        mfant = 'C:\\Program Files (x86)\\Micro Focus\\Enterprise Developer Build Toolsr\\bin\\mfant.jar'
    else:
        ant_home = '/opt/apache-ant-1.10.11'
        java_home = '/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.302.b08-0.el8_4.x86_64/jre'
        mfant = '/opt/microfocus/EnterpriseDeveloper/lib/mfant.jar'

    tasks_file = os.path.join(working_dir, '.vscode', 'tasks.json')
    tasks_json = read_json(tasks_file)

    build_json = get_elem_with_prop(tasks_json['tasks'], 'label', 'Build Program')
    build_env = build_json['options']['env']
    build_env['ANT_HOME'] = ant_home
    build_env['JAVA_HOME'] = java_home

    ant_args = build_json['args']
    lib_index = ant_args.index('-lib') + 1
    ant_args[lib_index] = mfant

    write_json(tasks_file, tasks_json)


if __name__ == "__main__":
    short_map = {}
    long_map = {
        '--WorkspaceFolder=': 'working_dir'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    init_course(**kwargs)
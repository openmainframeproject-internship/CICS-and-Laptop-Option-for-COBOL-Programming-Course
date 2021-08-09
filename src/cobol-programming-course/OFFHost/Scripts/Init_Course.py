#!/usr/bin/python3

"""
Author:  Josh Fogus
Description:  A script to initialize files based on the local system.
"""

import os
import sys
from shutil import copy2
from xml.etree import ElementTree
from utilities.misc import parse_args


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
    # 
    ##################




if __name__ == "__main__":
    short_map = {}
    long_map = {
        '--WorkspaceFolder=': 'working_dir'
    }

    kwargs = parse_args(sys.argv[1:], short_map, long_map)
    init_course(**kwargs)
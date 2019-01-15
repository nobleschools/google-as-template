#!python3

"""
Management function for a set of tools designed to work with Google Apps
Script API and Google Sheets
"""

import os
import sys
import yaml
from modules.gas import googleapi

SETTINGS = os.environ.setdefault('SETTINGSYAML', 'settings/settings.yaml')


def create_project(cfg):
    """
    Runs an authentication flow and then pushes an initial Apps Script file
    to the Google Drive folder specified in the Yaml file
    """
    creds = googleapi.get_credentials(cfg)
    print(creds)


def pull_scripts(cfg):
    """
    Makes local copies of all script files in the Drive folder configured
    in the Yaml file
    """
    # IMPLEMENT!
    print(cfg)


targets = {
    'create_project': create_project,
    'pull_scripts': pull_scripts,
}
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} [{}]'.format(
            sys.argv[0], '/'.join(targets.keys())
        ))
    else:
        with open(SETTINGS, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        targets[sys.argv[1]](cfg['google_settings'])
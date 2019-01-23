#!python3

"""
Management function for a set of tools designed to work with Google Apps
Script API and Google Sheets
"""

import os
import sys
import yaml
from apiclient import errors
from modules.gas import googleapi
from modules.gas import filework

SETTINGS = os.environ.setdefault('SETTINGSYAML', 'settings/settings.yaml')


def create_project(cfg):
    """
    Runs an authentication flow and then pushes an initial Apps Script file
    to the Google Drive folder specified in the Yaml file
    """
    creds = googleapi.Creds(cfg)
    service = creds.serv('script')

    try:
        # Create project
        request = {
            'title': cfg['script_name'],
            'parentId': cfg['project_dir']
            }
        response = service.projects().create(body=request).execute()

        # Upload files to the project
        files = [
            {'name': filename, 'type': 'SERVER_JS', 'source': code_body}
            for filename, code_body in
            filework.grab_js_files(cfg['local_script_dir']).items()
        ]
        files.append({'name': 'appsscript', 'type': 'JSON',
                     'source': filework.build_manifest(cfg)})
        # print(files)
        request = {'files': files}
        response = service.projects().updateContent(
            body=request,
            scriptId=response['scriptId']).execute()

        local_info = googleapi.ScriptSettings(cfg,
                                              scriptId=response['scriptId'])
        print(local_info)
        print('Script created. You will need to change the project to the')
        print('one used for this script. Find the project number here:')
        print('https://console.cloud.google.com/home/dashboard?project=' +
              creds.project)
        print('Then follow the steps in the README.')

    except errors.HttpError as error:
        print(error.content)


def explore(cfg):
    """
    Used for checking out the structure of the Google API (temporary)
    """
    local_info = googleapi.ScriptSettings(cfg)
    creds = googleapi.Creds(cfg)
    scriptId = local_info.get_script_id()
    creds = googleapi.Creds(cfg)
    service = creds.serv('script')
    proj = service.projects().deployments().list(scriptId=scriptId).execute()
    print(proj['deployments'][1])


def check_creation(cfg):
    """
    Simple target to run after creation to see if scripts can be run
    """
    local_info = googleapi.ScriptSettings(cfg)
    sid = local_info.get_api_id()
    creds = googleapi.Creds(cfg)
    service = creds.serv('script')
    request = {"function": "getFilesDirWithType",
               "parameters": [cfg['project_dir']],
               }
    out = googleapi.call_apps_script(request, service, sid)
    print('There are {} files in the folder'.format(len(out)))
    for k, v in out.items():
        name, mimetype = v.split(sep=':')
        print('{} (type {}) with key {}'.format(name, mimetype, k))


def pull_scripts(cfg):
    """
    Makes local copies of all script files in the Drive folder configured
    in the Yaml file
    """
    # IMPLEMENT!
    # Deploy and get sid
    # figure out project matching
    local_info = googleapi.ScriptSettings(cfg)
    sid = local_info.get_api_id()
    creds = googleapi.Creds(cfg)
    service = creds.serv('script')


targets = {
    'create_project': create_project,
    'check_creation': check_creation,
    'pull_scripts': pull_scripts,
    'explore': explore,
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

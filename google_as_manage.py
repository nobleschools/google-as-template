#!python3

"""
Management function for a set of tools designed to work with Google Apps
Script API and Google Sheets
"""

import os
import sys
import gspread
from apiclient import errors
from modules.gas import googleapi
from modules.gas import filework

SETTINGS = os.environ.setdefault('SETTINGSYAML', 'settings/settings.yaml')


def create_project(cfg):
    """
    Runs an authentication flow and then pushes an initial Apps Script file
    to the Google Drive folder specified in the Yaml file. Creates a
    local_settings.yaml file to hold the script id and api id. The latter
    has to be entered manually per the instructions in the README file.
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
        push_scripts(cfg, service=service, scriptId=response['scriptId'])
        """
        files = [
            {'name': filename, 'type': 'SERVER_JS', 'source': code_body}
            for filename, code_body in
            filework.grab_js_files(cfg['local_script_dir']).items()
        ]
        files.append({'name': 'appsscript', 'type': 'JSON',
                     'source': filework.build_manifest(cfg)})
        request = {'files': files}
        response = service.projects().updateContent(
            body=request,
            scriptId=response['scriptId']).execute()

        """
        local_info = googleapi.ScriptSettings(cfg,
                                              scriptId=response['scriptId'])
        print(local_info)
        local_info.store()
        print('Script created. You will need to change the project to the')
        print('one used for this script. Find the project number here:')
        print('https://console.cloud.google.com/home/dashboard?project=' +
              creds.project)
        print('Then follow the steps in the README.')

    except errors.HttpError as error:
        print(error.content)


def _inspect(obj):
    print('Inspecting {}'.format(type(obj)))
    try:
        for k, v in obj.items():
            print('Key: {}, Type: {}'.format(k, type(v)))
    except Exception as e:
        for x in dir(obj):
            print('Name: {}, Type: {}'.format(
                x, type(obj.__getattribute__(x))))
        raise e


def make_basic(cfg):
    """
    Create an initial Google Doc and demonstrate the capabilities of repo
    """
    scriptId = googleapi.ScriptSettings(cfg).get_script_id()
    creds = googleapi.Creds(cfg)
    service = creds.serv('script')
    gc = gspread.authorize(creds)
    new_doc = gc.create('test doc')



def explore(cfg):
    """
    Used for checking out the structure of the Google API (temporary)
    """
    scriptId = googleapi.ScriptSettings(cfg).get_script_id()
    creds = googleapi.Creds(cfg)
    service = creds.serv('script')
    proj = service.projects().deployments().list(scriptId=scriptId).execute()
    _inspect(proj)
    # print(proj['deployments'][0])
    # print(proj['deployments'][1])


def check_creation(cfg):
    """
    Simple target to run after creation to see if scripts can be run
    """
    sid = googleapi.ScriptSettings(cfg).get_api_id()
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


def push_scripts(cfg, service=None, scriptId=None):
    """
    Takes local copies of all script files and pushes them to the project.
    Note, this overwrites everything in the cloud version of the project.
    """
    if not service:
        creds = googleapi.Creds(cfg)
        service = creds.serv('script')
    if not scriptId:
        scriptId = googleapi.ScriptSettings(cfg).get_script_id()

    files = [
            {'name': filename, 'type': 'SERVER_JS', 'source': code_body}
            for filename, code_body in
            filework.grab_js_files(cfg['local_script_dir']).items()
        ]
    files.append({'name': 'appsscript', 'type': 'JSON',
                  'source': filework.build_manifest(cfg)})
    request = {'files': files}
    response = service.projects().updateContent(
        body=request,
        scriptId=scriptId
        ).execute()
    return response


def pull_scripts(cfg):
    """
    Makes local copies of all script files in the Drive folder configured
    in the Yaml file
    """
    creds = googleapi.Creds(cfg)
    response = creds.serv('script').projects().getContent(
        scriptId=googleapi.ScriptSettings(cfg).get_script_id()
        ).execute()
    print('Saving {} files locally'.format(len(response['files'])))
    for file in response['files']:
        filename = os.path.join(cfg['local_script_dir'], file['name'])
        filename += '.json' if file['name'] == 'appsscript' else '.js'
        filework.save_string_as_text_file(filename, file['source'])


# Global variables to define the targets for this tool
targets = {
    'make_basic': make_basic,
    'create_project': create_project,
    'check_creation': check_creation,
    'pull_scripts': pull_scripts,
    'push_scripts': push_scripts,
    'explore': explore,
}
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} [{}]'.format(
            sys.argv[0], '/'.join(targets.keys())
        ))
    else:
        cfg = filework.grab_yaml(SETTINGS)
        targets[sys.argv[1]](cfg['google_settings'])

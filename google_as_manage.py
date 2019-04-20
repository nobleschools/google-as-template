#!python3
"""
Management function for a set of tools designed to work with Google Apps
Script API and Google Sheets
"""

import os
import sys

from apiclient import errors
from modules.gas.struct_logger import get_logger
from modules.gas import googleapi
from modules.gas import filework

SETTINGS = os.environ.setdefault('SETTINGSYAML', 'settings/settings.yml')


def create_project(cfg):
    """
    Runs an authentication flow and then pushes an initial Apps Script file
    to the Google Drive folder specified in the Yaml file. Creates a
    local_settings.yaml file to hold the script id and api id. The latter
    has to be entered manually per the instructions in the README file.
    """
    creds = googleapi.Creds(cfg)
    service = creds.serv('script', cfg)

    try:
        # Create project
        request = {
            'title': cfg['script_name'],
            'parentId': cfg['project_dir']
            }
        cfg['logger'].info('Creating project', **request)
        response = service.projects().create(body=request).execute()

        # Upload files to the project
        push_scripts(cfg, service=service, scriptId=response['scriptId'])
        local_info = googleapi.ScriptSettings(cfg, scriptId=response['scriptId'])
        cfg['logger'].info(str(local_info))
        local_info.store()
        cfg['logger'].info('Script created. You will need to change the project to the')
        cfg['logger'].info('one used for this script. Find the project number here:')
        cfg['logger'].info('https://console.cloud.google.com/home/dashboard?project=' +
                           creds.project)
        cfg['logger'].info('Then follow the steps in the README.')

    except errors.HttpError as error:
        cfg['logger'].error(error.content)


def _inspect(obj):
    # DELETE WHOLE FUNCTION BEFORE 1.0
    print('Inspecting {}'.format(type(obj)))
    try:
        for k, v in obj.items():
            print('Key: {}, Type: {}'.format(k, type(v)))
    except Exception as e:
        for x in dir(obj):
            print('Name: {}, Type: {}'.format(
                x, type(obj.__getattribute__(x))))
        raise e


def explore(cfg):
    """
    Used for checking out the structure of the Google API (temporary)
    """
    # DELETE WHOLE FUNCTION BEFORE 1.0
    scriptId = googleapi.ScriptSettings(cfg).get_script_id()
    creds = googleapi.Creds(cfg)
    service = creds.serv('script', cfg)
    proj = service.projects().deployments().list(scriptId=scriptId).execute()
    print(scriptId)
    print(service)
    _inspect(proj)
    # print(proj['deployments'][0])
    # print(proj['deployments'][1])


def check_creation(cfg):
    """
    Simple target to run after creation to see if scripts can be run
    """
    sid = googleapi.ScriptSettings(cfg).get_api_id()
    creds = googleapi.Creds(cfg)
    service = creds.serv('script', cfg)
    request = {"function": "getFilesDirWithType",
               "parameters": [cfg['project_dir']],
               }
    out = googleapi.call_apps_script(request, service, sid, cfg)
    cfg['logger'].info('There are {} files in the folder'.format(len(out)))
    for k, v in out.items():
        name, mimetype = v.split(sep=':')
        cfg['logger'].info('File details', name=name, mimetype=mimetype, key=k)


def push_scripts(cfg, service=None, scriptId=None):
    """
    Takes local copies of all script files and pushes them to the project.
    Note, this overwrites everything in the cloud version of the project.
    """
    if not service:
        creds = googleapi.Creds(cfg)
        service = creds.serv('script', cfg)
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
    cfg['logger'].info('Pushing scripts', sub='push_scripts',
                       files=', '.join([x['name'] for x in files]))
    response = service.projects().updateContent(
        body=request,
        scriptId=scriptId
        ).execute()
    return response


def test_logging(cfg):
    """
    An example function to test the logging setup
    """
    cfg['logger'].debug('debug message')
    cfg['logger'].info('Here are cfg contents', **{k: str(v) for k, v in cfg.items()})
    cfg['logger'].warning('message', some_variable=1)
    cfg['logger'].error('error message')
    cfg['logger'].critical('critical message')


def pull_scripts(cfg):
    """
    Makes local copies of all script files in the Drive folder configured
    in the Yaml file
    """
    creds = googleapi.Creds(cfg)
    response = creds.serv('script', cfg).projects().getContent(
        scriptId=googleapi.ScriptSettings(cfg).get_script_id()
        ).execute()
    cfg['logger'].info('Saving {} files locally'.format(len(response['files'])))
    cfg['logger'].info('Filenames', sub='pull_scripts',
                       files=', '.join([f['name'] for f in response['files']]))
    for f in response['files']:
        filename = os.path.join(cfg['local_script_dir'], f['name'])
        filename += '.json' if f['name'] == 'appsscript' else '.js'
        filework.save_string_as_text_file(filename, f['source'])


# Global variables to define the targets for this tool
targets = {
    'create_project': create_project,
    'check_creation': check_creation,
    'pull_scripts': pull_scripts,
    'push_scripts': push_scripts,
    'explore': explore,  # kill this
    'test_logging': test_logging,
}
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} [{}]'.format(
            sys.argv[0], '/'.join(targets.keys())
        ))
    else:
        cfg = filework.grab_yaml(SETTINGS)
        logger = get_logger('gas_'+sys.argv[1], cfg['log_settings'])
        cfg['google_settings']['logger'] = logger
        targets[sys.argv[1]](cfg['google_settings'])

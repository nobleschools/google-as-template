#!python3

"""Functions for working with the Google API"""
import os
import json
import httplib2
from apiclient import discovery
from apiclient import errors
from oauth2client import tools
from oauth2client import client
from oauth2client.file import Storage
from modules.gas import filework


def get_credential_project(cfg):
    """Retrieves the project name for the current credentials"""
    secret_path = os.path.join(cfg['store_dir'], cfg['credentials_file'])
    cred_data = json.loads(filework.grab_file_as_text(secret_path))
    return cred_data['installed']['project_id']


def get_credentials(cfg):
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Assumes store_file is/will be and secret_file is in store_dir
    These and other constants passed via cfg dict from a startup yaml file

    Returns:
        credentials, the obtained credential.
    """
    credential_path = os.path.join(cfg['store_dir'], cfg['credentials_store'])
    store = Storage(credential_path)
    credentials = store.get()
    print('Credentials: {}'.format(str(credentials)))  # delete this later

    if not credentials or credentials.invalid:
        # Delete this later: trying to monitor intermittent failures
        print('Grabbing credentials a second time')
        credentials = store.get()

    if not credentials or credentials.invalid:
        secret_path = os.path.join(cfg['store_dir'], cfg['credentials_file'])
        flow = client.flow_from_clientsecrets(secret_path, cfg['scopes'])
        flow.user_agent = cfg['project_name']

        # This line keeps run_flow from trying to parse the command line
        flags = tools.argparser.parse_args([])
        credentials = tools.run_flow(flow, store, flags)
    return credentials


def get_service(service_type, version, creds):
    """Requests a service from the Google API"""
    http = creds.authorize(httplib2.Http())
    return discovery.build(service_type, version, http=http)


class ScriptSettings(object):
    """
    Class to hold local settings and construct/save locally
    to a YAML file
    """
    def __init__(self, cfg, scriptId='', apiId=''):
        self.local_settings = cfg['local_settings']
        if os.path.exists(self.local_settings):
            self.settings = filework.grab_yaml(self.local_settings)
        else:
            self.settings = {
                'scriptId': scriptId,
                'API ID': apiId,
            }

    def __repr__(self):
        return 'scriptId: '+self.settings['scriptId']

    def set_api_id(self, id):
        self.settings['API ID'] = id

    def get_script_id(self):
        return self.settings['scriptId']

    def get_api_id(self):
        return self.settings['API ID']

    def store(self):
        filework.store_yaml(self.local_settings, self.settings)


class Creds(object):
    """Class to house credentials and manage timeouts"""
    def __init__(self, cfg):
        self._creds = get_credentials(cfg)
        # Next two lines because the above fails sometimes
        if self._creds is None:
            print('In second get_credentials call inside object')
            self._creds = get_credentials(cfg)
        self._refresh_ttl = cfg['refresh_ttl']
        self._versions = cfg['service_versions']
        self.project = get_credential_project(cfg)

    def cred(self):
        """Returns the class variable, refreshing if close to expiring"""
        if self._creds._expires_in() < self._refresh_ttl:
            self._creds = self._creds.refresh(httplib2.Http())
        return self._creds

    def serv(self, service_type):
        return get_service(service_type,
                           self._versions[service_type],
                           self.cred())


def output_script_error(error):
    """
    Cleanly outputs an error return from an Apps Script API call
    """
    print('Script error message: %s' % str(error['errorMessage']))
    if 'scriptStackTraceElements' in error:
        print('Script error stacktrace:')
        for trace in error['scriptStackTraceElements']:
            print('\t%s: %s' % (str(trace['function']),
                                str(trace['lineNumber'])))
    return 'Error'


def call_apps_script(request, service, script_id,
                     error_handler=output_script_error,
                     dev_mode="true"):
    """
    Helper function to call app_script and manage any errors
    """
    request["devMode"] = dev_mode  # runs latest save if true (vs deployment)
    try:
        response = service.scripts().run(
            body=request,
            scriptId=script_id).execute()
        if 'error' in response:
            # Here, the script is returning an error
            return error_handler(response['error']['details'][0])
        else:
            return response['response'].get('result', {})

    except errors.HttpError as e:
        # Here, the script likely didn't execute: there was an error prior
        print(e.content)
        raise

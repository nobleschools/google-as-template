#!python3
"""
Unit tests for the google-as-template base
"""
import os
import yaml
SETTINGS = os.environ.setdefault('SETTINGSYAML', 'settings/settings.yaml')


class TestYaml(object):
    def test_that_yaml_file_exists(self):
        # There should be a master yaml file: settings/settings.yaml
        # It will have basic google drive info inside
        with open(SETTINGS, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        assert 'google_settings' in cfg


class TestGoogleApps(object):
    def setup_method(self):
        with open(SETTINGS, 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)
            self.folder = self.cfg['google_settings']['project_dir']
            self.script = self.cfg['google_settings']['script_name']

    def teardown_method(self):
        pass

    def test_can_see_apps_script_file(self):
        assert self.script == 'Apps Scripts'

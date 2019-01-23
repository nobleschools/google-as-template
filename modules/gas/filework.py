#!python3

"""Functions for doing the filesystem work related with google-as-template"""
import os
import yaml


def grab_yaml(fn):
    with open(fn, 'r') as ymlfile:
        return yaml.load(ymlfile)


def store_yaml(fn, data_dict):
    with open(fn, 'w') as ymlfile:
        yaml.dump(data_dict, ymlfile, default_flow_style=False)


def save_string_as_text_file(fn, data):
    with open(fn, 'w') as f:
        f.write(data)


def grab_file_as_text(fn):
    with open(fn, 'r') as f:
        return f.read().strip()


def grab_js_files(js_dir):
    """Returns a dict of script files for building a project"""
    return {
        fn[:-3]: grab_file_as_text(os.path.join(js_dir, fn))
        for fn in os.listdir(js_dir) if fn.endswith('.js')
        }


def build_manifest(cfg):
    """Returns the JSON manifest for a new project either from file or cfg"""
    manifest_file = os.path.join(cfg['local_script_dir'], 'appsscript.json')
    if os.path.exists(manifest_file):
        return grab_file_as_text(manifest_file)
    else:
        return '{\n  "timeZone": "{}"\n}'.format(cfg['project_tz'])

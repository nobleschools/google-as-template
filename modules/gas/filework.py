#!python3

"""Functions for doing the filesystem work related with google-as-template"""
import os


def grab_file_as_text(fn):
    with open(fn, 'r') as f:
        return f.read().strip()


def grab_js_files(js_dir):
    """Returns a dict of script files for building a project"""
    return {
        fn.replace('.js', '.gs'): grab_file_as_text(os.path.join(js_dir, fn))
        for fn in os.listdir(js_dir) if fn.endswith('.js')
        }


def build_manifest(cfg):
    """Returns the JSON manifest for a new project either from file or cfg"""
    return '{\n  "timeZone": "TZ"\n}'.replace('TZ', cfg['project_tz'])

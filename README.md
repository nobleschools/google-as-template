# google-as-template
Base configuration for working with Google Apps Scripts for Google Docs trackers, etc

---
## Overview

This repo is designed as a starting off point for projects that use Google
Apps Scripts, primarily for access with Google Spreadsheets. It has few
features:

1. Yaml template defining the project
2. Helper scripts to clone/push apps scripts locally for source control
3. Integration with logging and pytest
4. Standard API functions and AppsScripts designed for spreadsheet projects

---

## Getting started

1. Go to the [Google Apps Script API Python Quickstart](https://developers.google.com/apps-script/api/quickstart/python)
   and follow "Step 1" to create a new console project, enable the API and
   receive credentials. Place the "credentials.json" file in a '.credentials'
   folder off the main directory. Also, note the new project name for later.
2. Edit the settings/settings.yaml file as follows (all in google_settings):
  1. Change the project_name setting to the one you created in Step 1.
  2. Change the project_dir setting to the key for your Google Drive folder
  3. Change the default script name in script_name
  4. Modify any of the remaining defaults if necessary (especially scopes)
3. Run 'python google_as_manage.py create_project' to do an initial
   authentication and then push a starter script into your project directory.
4. Run 'python google_as_manage.py pull_scripts' to copy the Google Drive
   scripts into your local scripts folder for inclusion into version control.
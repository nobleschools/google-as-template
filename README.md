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
   A few notes:
   - If the authentication doesn't work via your local browser, you might
     need to specify a command line option.
   - Depending on what you've done before, you might need to enable the
     specific APIs in you Google account. If this occurs, the script will
     prompt with an error message indicating the URL to do so.
4. In order to run these scripts with the API, you'll need to create a
   "Deployment" in the newly created project file:
   - Go to Publish->Deploy as API executable...
   - In the "Describe this version" prompt, enter "Initial version"
   - Select "Anyone" in the "Who has access to the script" section
   - Click "Continue if there's a warning
   - Copy the "Current API ID" value and replace the '' in
     settings/local_settings.yaml next to 'API ID' with this value 
     then hit close.
5. At the exit of the "create_project" step, a message will print telling you
   to change the project of the newly created script. In order to execute the
   script using the credentials you already have, you'll need both to have same
   project.
   - Go to the link printed by create_project. If you have multiple Google
     accounts, you might need to switch to the correct account.
   - Copy the "Project Number" under the "Project Info section on the left
   - Go to the newly created script and go to Resources->Cloud Platform
     project...
   - In this dialog, enter the project number you just copied into the blank
     under "Change Project" and then click "Set Project". Hit "Confirm".
   - Close the dialog. You should be ready to execute.

6. Run 'python google_as_manage.py check_creation' to see if everything is
   working. This should list out all of the files in the project folder.

---

## Apps Script tools

### python google_as_manage.py pull_scripts
_and_
### python google_as_manage.py push scripts

The first function allows you to pull scripts from the Google Script project
to the local scripts folder (so you can package or push to git.)

The second does the opposite, allowing you to overwrite the online project
with the local script files.

_Both functions a "destructive" and overwrite the destination._

---

## Usage for running script functions

xx

---

## Extra tools for working with Google Sheets

xx


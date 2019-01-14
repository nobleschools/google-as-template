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
   receive credentials. Place the "credentials.json" file in this main
   directory. Also, note the new project name for later.
2. Stuff
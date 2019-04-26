#!python3

"""
Script to provide an example of the uses for this repository.

Assumes you've already setup a project as described in the project readme.
The commenting in this file is more verbose than normal to aid in new developers
being able to follow along.
"""
import os
import shutil
import csv

from modules.gas.struct_logger import get_logger
from modules.gas import googleapi
from modules.gas import filework
from google_as_manage import push_scripts

# These are all of the settings
SETTINGS = os.environ.setdefault('SETTINGSYAML', 'settings/settings.yml')
EXAMPLE_DATA = 'example/example_data.csv'
EXAMPLE_SCRIPT = 'example/example_as.js'
OUTPUT_CSV = 'example/summary_output.csv'
OUTPUT_CSV2 = 'example/summary_output_gspread.csv'


def main(cfg):
    """
    Logging was setup in the call to main along with the reading of the yaml settings
    file (which contains google settings)
    """
    cfg['logger'].info('Running example script for google-as-template')

    # This next line creates an object we use whenever we need to get credentials.
    # We use a class in order to make sure it's reauthorizing when it gets close to
    # timing out.
    creds = googleapi.Creds(cfg)

    # The line above is only called once, but everytime we want to use credentials,
    # we access them through the cred() method as below.

    # gc stands for 'google client' and is the main class for working with the gspread
    # library. In the below, we'll use both. gspread is best for bigger actions
    # relating to Google Sheets (creating them, adding tabs, etc.) while Apps Scripts
    # are best for more detailed work, particularly when it comes to formatting.
    gc = creds.gspread_client()

    # This line creates a brand new Google sheet in the user's home dir
    # We won't be using 'gc' much below this, working instead with the spreadsheet
    # object (new_doc)
    new_doc = gc.create('Example Sheet File')

    # These two lines move the file to the project dir and then change the permissions
    # so that anyone with the link can edit. Note that we're requesting a service
    # separately in both lines. Doing this instead of reusing a local variable causes
    # the api to check each time to make sure that the access token isn't close to
    # timing out.
    googleapi.move_file(new_doc.id, cfg['project_dir'], creds.serv('drive', cfg), cfg)
    googleapi.add_link_permissions(new_doc.id, creds.serv('drive', cfg), cfg)

    # Now, we'll load the example file into the first tab of the sheet
    # This first method is a quick way to do it via gspread, but has some limitations
    cfg['logger'].info('Writing example csv data to the first tab')
    example_data = open(EXAMPLE_DATA, 'r').read()
    gc.import_csv(new_doc.id, example_data)
    new_doc.sheet1.update_title('Raw_csv_sheet')

    # As a second method, we'll load the same data, but manipulate the csv data as a
    # list of lists first (and use a different method to load it)
    cfg['logger'].info('Writing same csv data to the second tab with lol function')
    with open(EXAMPLE_DATA, 'r') as f:
        reader = csv.reader(f)
        l_o_l_csv_data = [row for row in reader]
    ws = new_doc.add_worksheet('Written_csv_sheet',
                               len(l_o_l_csv_data), len(l_o_l_csv_data[0]))

    # The function below will write the data to a sheet using the update_cells method
    # in the gspread library. It's more efficient for sparse data.
    googleapi.write_lol_to_sheet(ws, l_o_l_csv_data, cfg)

    # As yet a third method, we'll send it to an AppsScript function directly
    cfg['logger'].info('Writing same csv data to the third tab with writeData')

    # For fun, we'll add a column that counts the number of characters in the name
    l_o_l_csv_data[0].insert(2, 'Name length')
    for i in range(1, len(l_o_l_csv_data)):
        l_o_l_csv_data[i].insert(2, '=len(B'+str(i+1)+')')
    ws = new_doc.add_worksheet('AS_written_csv',
                               len(l_o_l_csv_data), len(l_o_l_csv_data[0]))

    # This calls a function that was part of the utilities.js file that was pushed
    # to the Apps Script project when you ran the setup
    googleapi.call_apps_script(
        {"function": "writeDataTable",
         "parameters": [new_doc.id, 'AS_written_csv', l_o_l_csv_data]
         },
        creds.serv('script', cfg), cfg)

    # Now, we'd like to format this last tab. Formatting requires Apps Script, so we'll
    # Need to push an appscript file to the project and then run it.
    # This push script (and the pull script) were intended primarily for syncing with
    # git via the command line, but you can use them programmatically like below
    cfg['logger'].info('Copying example script to project dir and pushing to remote.')
    shutil.copy(EXAMPLE_SCRIPT, cfg['local_script_dir'])
    push_scripts(cfg)

    googleapi.call_apps_script(
        {"function": "doExampleFormatting",
         "parameters": [new_doc.id, 'AS_written_csv']
         },
        creds.serv('script', cfg), cfg)

    # In addition to the saving of data tables, we can write new summary or other
    # more structured tabs to sheets directly. Here, we'll create a tab that
    # summarizes the number of presidents from each state
    pres_states = [x[7] for x in l_o_l_csv_data[1:]]
    pres_states = list(set(pres_states))  # Reduce to unique values, one per state
    pres_states.sort()
    num_states = len(pres_states)
    cfg['logger'].info('Adding a tab that counts states.', pres_states=str(pres_states))

    rows = 4 + num_states  # Title row at top, header row, sum row, blank row
    cols = 5  # Blank column, state, count, count since 1900, blank column
    ws = new_doc.add_worksheet('State_summary', rows, cols)
    output_matrix = [
        (1, 1, 'Summary of Presidents by state'),
        (2, 2, 'State'),
        (2, 3, 'Number of presidents'),
        (2, 4, 'Number since 1900'),
    ]
    for i in range(num_states):
        output_matrix.extend([
            (i+3, 2, pres_states[i]),
            (i+3, 3, '=COUNTIF(HomeState,B'+str(i+3)+')'),
            (i+3, 4, '=COUNTIFS(HomeState,B'+str(i+3)+',StartDate,">1/1/1900")')
        ])
    output_matrix.extend([
        (num_states+3, 2, 'Total'),
        (num_states+3, 3, '=SUM(C3:C'+str(num_states+2)+')')
    ])  # There's one other summary, but we'll demonstrate that in the Apps Script

    googleapi.send_bulk_data(ws, output_matrix, cfg)
    googleapi.call_apps_script(
        {"function": "formatSummarySheet",
         "parameters": [new_doc.id, 'State_summary', len(pres_states)]
         },
        creds.serv('script', cfg), cfg)

    # Finally, let's read the data from the tables and save it locally
    # One approach is to use the Apps Script function included in the setup:
    cfg['logger'].info('Saving summary tab to csv using two different methods',
                       filename1=OUTPUT_CSV, filename2=OUTPUT_CSV2)
    raw_data = googleapi.call_apps_script(
        {"function": "readDataTable",
         "parameters": [new_doc.id, 'State_summary']
         },
        creds.serv('script', cfg), cfg)
    processed_data = [x[1:4] for x in raw_data[1:]]  # Filter out the non-data cells
    save_lol_as_csv(OUTPUT_CSV, processed_data)

    # A second approach is to use the built-in function in gspread:
    raw_data = ws.get_all_values()
    processed_data = [x[1:4] for x in raw_data[1:]]  # Exactly the same as above
    save_lol_as_csv(OUTPUT_CSV2, processed_data)


def save_lol_as_csv(fn, lol):
    """Utility function to save a list of lists as a csv"""
    with open(fn, 'wt', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL,
                            lineterminator='\n')
        for row in lol:
            writer.writerow(row)


if __name__ == '__main__':
    # See comments in the yaml file itself for the standard settings
    cfg = filework.grab_yaml(SETTINGS)

    # This line sets up logging with structlog and stdout+remote logging
    logger = get_logger('gas_example', cfg['log_settings'])

    # There are different approaches, but maybe the cleanest way to persist logging
    # across multiple modules is to pass a reference to the actual object (in a dict)
    # Because we're already passing a dict with configuration settings from module
    # to module, we're stashing the logger in this 'cfg' dict for convenience
    cfg['google_settings']['logger'] = logger

    # Note that in the main function, we're ignoring any yaml settings not in this key
    main(cfg['google_settings'])

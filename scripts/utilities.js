// Default utitilites file for google-as-template

//---------------------------- Script functions ---------------
/*
 * Test function
 */
function helloWorld() {
    console.log("Hello, world!");
    console.log("Hello again!");
  }

//---------------------------- Manipulation/variable functions ---------------
/**
 * getDataRowsList:
 * takes an object[][] and returns an array of object literals (lists)
 */
function getDataRowsList(values) {
  var objects = [];
  for (var i=0; i<values.length; i++){
    var object = [];
    for (var j=0; j<values[i].length; j++){
      object.push(values[i][j]);
    }
    objects.push(object);
  }
  return objects;
}

//---------------------------- Sheets functions ---------------
/**
 * resizeSheet:
 * takes a sheet and desired rows and columns and resizes to that size
 * Adds and deletes at the end for either
 */
function resizeSheet(sheet, rows, cols) {
  var currentRows = sheet.getMaxRows();
  var currentColumns = sheet.getMaxColumns();
  
  if (rows > currentRows) {
    sheet.insertRowsAfter(currentRows, (rows - currentRows));
  } else if (rows < currentRows) {
    sheet.deleteRows(rows+1, (currentRows-rows));
  }
  if (cols > currentColumns) {
    sheet.insertColumnsAfter(currentColumns, (rows - currentColumns));
  } else if (cols < currentColumns) {
    sheet.deleteColumns(cols+1, (currentColumns-cols));
  }
}

/**
 * writeDataTable:
 * Writes a array of arrays (list of lists) to the upper left cells of a sheet
 * Will resize to match the width of the first rows
 **/
function writeDataTable(ss_key, s_name, values) {
  var ss = SpreadsheetApp.openById(ss_key);
  var sheet = ss.getSheetByName(s_name);
  
  var num_rows = values.length;
  var num_cols = values[0].length;
  
  resizeSheet(sheet, num_rows, num_cols);
  
  // The values below are pushed out with sanitizing them
  var write_range = sheet.getRange(1,1,num_rows,num_cols);
  write_range.setValues(values);
}

/**
* isValidDate:
 * From http://stackoverflow.com/questions/1353684
 * Returns 'true' if variable d is a date object, 'false' otherwise.
 **/
function isValidDate(d) {
  if ( Object.prototype.toString.call(d) !== "[object Date]" )
    return false;
  return !isNaN(d.getTime());
}

/**
 * readDataTable:
 * Reads a list of lists from the upper left cells of a sheet
 * and returns the values. If called without max_cols, will
 * assume a default value (extra wide sheets have a risk of
 * timing out during reads)
 **/
function readDataTable(ss_key, s_name, max_cols) {
  var ss = SpreadsheetApp.openById(ss_key);
  var sheet = ss.getSheetByName(s_name);
  if (max_cols === undefined) {max_cols = 53;}
  
  if (sheet == null) {
    return [['NULL']];
  } else {
    var lr = sheet.getLastRow();
    var lc = sheet.getLastColumn();
  
    // Extra wide sheets may timeout, so this solves for that
    if (lc > max_cols) { lc = max_cols; }
  
    var all_values = sheet.getRange(1,1,lr,lc).getValues();
    
    //Now we need to clean the return for dates
    for (var i=0; i<all_values.length; i++) {
      for (var j=0; j<all_values[i].length; j++) {
        if (isValidDate(all_values[i][j])) {
          all_values[i][j] = Utilities.formatDate(new Date(all_values[i][j]), "CST", "MM/dd/yyyy");
        }
      }
    }
    
    return all_values;
  }
}

// ----------------------------------- Drive functions ----------------------
/**
 * getFoldersUnderRoot:
 * Return the set of folder names contained in the user's root folder as an
 * object (with folder IDs as keys).
 * @return {Object} A set of folder names keyed by folder ID.
 */
function getFoldersUnderRoot() {
  var root = DriveApp.getRootFolder();
  var folders = root.getFolders();
  var folderSet = {};
  while (folders.hasNext()) {
    var folder = folders.next();
    folderSet[folder.getId()] = folder.getName();
  }
  return folderSet;
}

/**
 * getFilesDir:
 * Return the set of file names contained in the passed folder as an
 * object (with file IDs as keys).
 * @return {Object} A set of file names keyed by file ID.
 */
function getFilesDir(folder_key) {
  var folder = DriveApp.getFolderById(folder_key);
  var files = folder.getFiles();
  var fileSet = {};

  while (files.hasNext()) {
    var file = files.next();
    fileSet[file.getId()] = file.getName();
  }
  return fileSet;
}

/**
 * getFilesDirWithType:
 * Return the set of file names with MIME Type contained in the passed folder
 * as an object (with folder IDs as keys and file names concatentated to type).
 * @return {Object} A set of file names keyed by file ID.
 */
function getFilesDirWithType(folder_key) {
  var folder = DriveApp.getFolderById(folder_key);
  var files = folder.getFiles();
  var fileSet = {};

  while (files.hasNext()) {
    var file = files.next();
    fileSet[file.getId()] = file.getName()+':'+file.getMimeType();
  }
  return fileSet;
}
// Default utitilites file for google-as-template

//---------------------------- Script functions ---------------
/*
 * Test function
 */
function helloWorld() {
    console.log("Hello, world!");
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
function getFilesDir(folder_key) {
  var folder = DriveApp.getFolderById(folder_key);
  var files = folder.getFiles();
  var fileSet = {};

  while (files.hasNext()) {
    var file = files.next();
    fileSet[file.getId()] = file.getName()+':'+file.getMimeType();
  }
  return fileSet;
}

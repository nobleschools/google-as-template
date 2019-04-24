// Apps Script code for use with the google-as-template example script

/**
 * doExampleFormatting:
 * Formats the final sheet in this example, also writing a final formula
 **/
function doExampleFormatting(ssKey, sheetName) {
  var ss = SpreadsheetApp.openById(ssKey);
  var sheet = ss.getSheetByName(sheetName);
  
  // If we didn't know the sheet was the same length as data, we could pass this
  var lr = sheet.getLastRow();
  
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(1);
  
  sheet.getRange('A1:H1').setFontWeight('bold');
  sheet.getRange('A1:H1').setWrap(true);
  
  sheet.setColumnWidth(1,76);
  sheet.setColumnWidth(2,172);
  sheet.setColumnWidth(3,81);
  sheet.setColumnWidth(4,302);
  sheet.setColumnWidths(5,2,70);
  sheet.hideColumns(7,2);
  
  sheet.getRange('C2:C'+lr).setHorizontalAlignment('center');
  sheet.getRange('E2:F'+lr).setNumberFormat('M/d/yyyy');
  
  ss.setNamedRange('HomeState',sheet.getRange('H2:H'+lr));
  ss.setNamedRange('StartDate',sheet.getRange('E2:E'+lr));
}


/**
 * formatSummarySheet:
 * Formats the final sheet in this example, also writing a final formula
 **/
function formatSummarySheet(ssKey, sheetName, numStates) {
  var ss = SpreadsheetApp.openById(ssKey);
  var sheet = ss.getSheetByName(sheetName);
  
  // This is the final row for a total row after all states
  var lr = 3 + numStates;
  
  //sheet.getRange('A1:D2').setFontWeight('bold');
  sheet.getRange('A1').setFontSize(14);
  sheet.getRange('B2:D2').setWrap(true);
  
  sheet.setColumnWidth(1,20);
  sheet.setColumnWidth(2,150);
  sheet.setColumnWidths(3,2,80);
  
  // We'd normally do this from the Python, but demonstrating here:
  sheet.getRange('D'+lr).setValue('=SUM(D3:D'+(lr-1)+')')
  
  sheet.getRange('C2:D'+lr).setHorizontalAlignment('center');
  
  // With the bold cells, we'll demonstrate covering the same formatting in discrete cells
  var boldArray = ["A1", "B2", "C2", "D2", "B"+lr, "C"+lr, "D"+lr];
  for (var i = 0; i < boldArray.length; i++) {
    sheet.getRange(boldArray[i]).setFontWeight('bold');
  }
  
  //Make boxes
  var boxArray = ["B2:D"+lr, "B"+lr+":D"+lr];
  for (var i = 0; i < boxArray.length; i++) {
    sheet.getRange(boxArray[i]).setBorder(true,true,true,true,null,null);
  }
}
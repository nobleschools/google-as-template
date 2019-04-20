function doExampleFormatting(ssKey, sheetName) {
  // Does the formatting for this example tab
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
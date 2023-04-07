function insertTotalValues() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var numColumns = sheet.getMaxColumns();
    var data = sheet.getRange(1, 1, numRows, numColumns).getValues();

    // Find the first empty row
    var firstEmptyRow = -1;
    for (var i = 0; i < data.length; i++) {
        if (
            data[i].every(function (cell) {
                return cell === "";
            })
        ) {
            firstEmptyRow = i + 1;
            break;
        }
    }

    if (firstEmptyRow === -1) {
        // If the sheet is full, add a new row at the end
        sheet.insertRowAfter(numRows);
        firstEmptyRow = numRows + 1;
    }

    // Insert "total" in Column A
    sheet.getRange(firstEmptyRow, 1).setValue("total");

    // Calculate the sum for columns D, E, and H
    var sumD = sheet
        .getRange(2, 4, firstEmptyRow - 2, 1)
        .getValues()
        .reduce(function (a, b) {
            return a + b[0];
        }, 0);
    var sumE = sheet
        .getRange(2, 5, firstEmptyRow - 2, 1)
        .getValues()
        .reduce(function (a, b) {
            return a + b[0];
        }, 0);
    var sumH = sheet
        .getRange(2, 8, firstEmptyRow - 2, 1)
        .getValues()
        .reduce(function (a, b) {
            return a + b[0];
        }, 0);

    // Fill out the empty cells with the calculated values
    sheet.getRange(firstEmptyRow, 4).setValue(sumD);
    sheet.getRange(firstEmptyRow, 5).setValue(sumE);
    sheet.getRange(firstEmptyRow, 8).setValue(sumH);
}

function formatColumnA() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnA = sheet.getRange(2, 1, numRows - 1, 1); // Start from row 2 to exclude the header
    var values = columnA.getValues();

    for (var i = 0; i < values.length; i++) {
        var cell = columnA.getCell(i + 1, 1);
        var value = values[i][0].toString().toLowerCase();

        if (value.endsWith("robinhood")) {
            cell.setBackground("#38761d").setFontColor("white");
        } else if (value.endsWith("coinbase")) {
            cell.setBackground("#1155cc").setFontColor("white");
        } else if (value.endsWith("coinbase_pro")) {
            cell.setBackground("#434343").setFontColor("white");
        } else if (value.endsWith("kraken")) {
            cell.setBackground("#674ea7").setFontColor("white");
        } else if (value === "total") {
            cell.setBackground("#fce8b2")
                .setFontColor("black")
                .setFontWeight("bold");
        }
    }
}

function formatDateColumns() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();

    // Format Column B - Date Acquired
    var columnB = sheet.getRange(2, 2, numRows - 1, 1); // Start from row 2 to exclude the header
    columnB.setNumberFormat("M/d/yyyy");

    // Format Column C - Date Sold or Disposed of
    var columnC = sheet.getRange(2, 3, numRows - 1, 1); // Start from row 2 to exclude the header
    columnC.setNumberFormat("M/d/yyyy");
}

function formatCurrencyColumns() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();

    // Columns to format as currency: D, E, G, H
    var columnsToFormat = [4, 5, 7, 8];

    columnsToFormat.forEach(function (column) {
        var range = sheet.getRange(2, column, numRows - 1, 1); // Start from row 2 to exclude the header
        range.setNumberFormat("$#,##0.00");
    });
}

function formatColumnH() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnH = sheet.getRange(2, 8, numRows - 1, 1); // Start from row 2 to exclude the header
    var values = columnH.getValues();

    for (var i = 0; i < values.length; i++) {
        var cell = columnH.getCell(i + 1, 1);
        var value = values[i][0];

        if (value > 0) {
            cell.setBackground("#b7e1cd");
        } else if (value < 0) {
            cell.setBackground("#f4c7c3");
        } else if (value === 0) {
            cell.setBackground("#fce8b2");
        }
    }
}

function formatData() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Get the number of rows and columns in the sheet
    var numRows = sheet.getMaxRows();
    var numColumns = sheet.getMaxColumns();

    // Left align columns A, B, and C
    var leftAlignedColumns = sheet.getRange(1, 1, numRows, 3);
    leftAlignedColumns.setHorizontalAlignment("left");

    // Right align columns D, E, G, and H
    var rightAlignedColumns1 = sheet.getRange(1, 4, numRows, 2);
    rightAlignedColumns1.setHorizontalAlignment("right");
    var rightAlignedColumns2 = sheet.getRange(1, 7, numRows, 2);
    rightAlignedColumns2.setHorizontalAlignment("right");

    // Center align the header row
    var headerRow = sheet.getRange(1, 1, 1, numColumns);
    headerRow.setHorizontalAlignment("center");

    // Make the header row bold
    headerRow.setFontWeight("bold");

    // Freeze the header row
    sheet.setFrozenRows(1);

    // Auto resize columns A - H
    sheet.autoResizeColumns(1, 8);

    insertTotalValues();
    formatColumnA();
    formatDateColumns();
    formatCurrencyColumns();
    formatColumnH();
}

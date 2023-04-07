function formatColumnA() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnA = sheet.getRange(2, 1, numRows - 1, 1); // Start from row 2 to exclude the header
    var values = columnA.getValues();

    for (var i = 0; i < values.length; i++) {
        var cell = columnA.getCell(i + 1, 1);
        var value = values[i][0].toString().toLowerCase();

        if (value === "coinbase") {
            cell.setBackground("#1155cc").setFontColor("white");
        } else if (value === "coinbase_pro") {
            cell.setBackground("#434343").setFontColor("white");
        } else if (value === "kraken") {
            cell.setBackground("#674ea7").setFontColor("white");
        } else if (value === "atm") {
            cell.setBackground("#990000").setFontColor("white");
        } else if (value === "total") {
            cell.setBackground("#fce8b2")
                .setFontColor("black")
                .setFontWeight("bold");
        }
    }
}

function formatDateTimeColumns() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();

    // Format column C as Date time
    var columnC = sheet.getRange(1, 3, numRows, 1);
    columnC.setNumberFormat("M/d/yyyy H:mm:ss");

    // Format column J as Date time
    var columnJ = sheet.getRange(1, 10, numRows, 1);
    columnJ.setNumberFormat("M/d/yyyy H:mm:ss");
}

function formatColumnD() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnD = sheet.getRange(2, 4, numRows - 1, 1); // Start from row 2 to exclude the header
    var values = columnD.getValues();

    for (var i = 0; i < values.length; i++) {
        var cell = columnD.getCell(i + 1, 1);
        var value = values[i][0].toString().toLowerCase();

        if (value === "buy") {
            cell.setBackground("#b7e1cd");
        } else if (value === "sell") {
            cell.setBackground("#f4c7c3");
        }
    }
}

function formatColumnE() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnE = sheet.getRange(2, 5, numRows - 1, 1); // Start from row 2 to exclude the header
    var customNumberFormat = "0.00000000"; // Custom number format with a precision of 1 * 10 ^ -8

    columnE.setNumberFormat(customNumberFormat);
}

function formatCurrencyColumns() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();

    // Format Columns F, G, H, and I
    var currencyColumns1 = sheet.getRange(2, 6, numRows - 1, 4); // Start from row 2 to exclude the header
    currencyColumns1.setNumberFormat("$0.00");

    // Format Columns K and L
    var currencyColumns2 = sheet.getRange(2, 11, numRows - 1, 2); // Start from row 2 to exclude the header
    currencyColumns2.setNumberFormat("$0.00");
}

function formatColumnK() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnK = sheet.getRange(2, 11, numRows - 1, 1); // Start from row 2 to exclude the header
    var values = columnK.getValues();

    for (var i = 0; i < values.length; i++) {
        var cell = columnK.getCell(i + 1, 1);
        var value = values[i][0];

        if (value > 0) {
            cell.setBackground("#fce8b2");
        }
    }
}

function formatColumnL() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnL = sheet.getRange(2, 12, numRows - 1, 1); // Start from row 2 to exclude the header
    var values = columnL.getValues();

    for (var i = 0; i < values.length; i++) {
        var cell = columnL.getCell(i + 1, 1);
        var value = values[i][0];

        if (value > 0) {
            cell.setBackground("#b7e1cd");
        } else if (value < 0) {
            cell.setBackground("#f4c7c3");
        }
    }
}

function formatColumnM() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var numRows = sheet.getMaxRows();
    var columnM = sheet.getRange(2, 13, numRows - 1, 1); // Start from row 2 to exclude the header
    var values = columnM.getValues();

    for (var i = 0; i < values.length; i++) {
        var cell = columnM.getCell(i + 1, 1);
        var value = values[i][0];

        if (value) {
            cell.setBackground("#fce8b2");
        }
    }
}

function formatData() {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Get the number of rows and columns in the sheet
    var numRows = sheet.getMaxRows();
    var numColumns = sheet.getMaxColumns();

    // Left align columns A, B, C, J, and M
    var leftAlignedColumns1 = sheet.getRange(1, 1, numRows, 3);
    leftAlignedColumns1.setHorizontalAlignment("left");
    var leftAlignedColumns2 = sheet.getRange(1, 10, numRows, 1);
    leftAlignedColumns2.setHorizontalAlignment("left");
    var leftAlignedColumns3 = sheet.getRange(1, 13, numRows, 1);
    leftAlignedColumns3.setHorizontalAlignment("left");

    // Center align column D
    var centerAlignedColumn = sheet.getRange(1, 4, numRows, 1);
    centerAlignedColumn.setHorizontalAlignment("center");

    // Right align columns E, F, G, H, I, K, and L
    var rightAlignedColumns1 = sheet.getRange(1, 5, numRows, 4);
    rightAlignedColumns1.setHorizontalAlignment("right");
    var rightAlignedColumns2 = sheet.getRange(1, 11, numRows, 2);
    rightAlignedColumns2.setHorizontalAlignment("right");

    // Center align the header row
    var headerRow = sheet.getRange(1, 1, 1, numColumns);
    headerRow.setHorizontalAlignment("center");

    // Make the header row bold
    headerRow.setFontWeight("bold");

    // Freeze the header row
    sheet.setFrozenRows(1);

    // Auto resize columns A - M
    sheet.autoResizeColumns(1, 13);

    formatColumnA();
    formatDateTimeColumns();
    formatColumnD();
    formatColumnE();
    formatCurrencyColumns();
    formatColumnK();
    formatColumnL();
    formatColumnM();
}

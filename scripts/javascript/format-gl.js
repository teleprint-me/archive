// CELL_COLORS and EXCHANGE_COLORS are available in global namespace
function formatGainsLosses() {
    const LEFT_ALIGNED_COLUMNS = [1, 2, 3, 10, 13];
    const CENTER_ALIGNED_COLUMNS = [4];
    const RIGHT_ALIGNED_COLUMNS = [5, 6, 7, 8, 9, 11, 12];
    const DATE_COLUMNS = [3, 10];
    const HEADER_ROW = 1;
    const FIRST_DATA_ROW = HEADER_ROW + 1;

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Get the number of rows and columns in the sheet
    var numRows = sheet.getMaxRows();
    var numColumns = sheet.getMaxColumns();

    function leftAlignColumns() {
        LEFT_ALIGNED_COLUMNS.forEach(function (column) {
            var leftAlignedColumn = sheet.getRange(1, column, numRows, 1);
            leftAlignedColumn.setHorizontalAlignment('left');
        });
    }

    function centerAlignColumns() {
        CENTER_ALIGNED_COLUMNS.forEach(function (column) {
            var centerAlignedColumn = sheet.getRange(1, column, numRows, 1);
            centerAlignedColumn.setHorizontalAlignment('center');
        });
    }

    function rightAlignColumns() {
        RIGHT_ALIGNED_COLUMNS.forEach(function (column) {
            var rightAlignedColumn = sheet.getRange(1, column, numRows, 1);
            rightAlignedColumn.setHorizontalAlignment('right');
        });
    }

    function formatHeaderRow() {
        // Center align the header row
        var headerRow = sheet.getRange(1, 1, 1, numColumns);
        headerRow.setHorizontalAlignment('center');

        // Make the header row bold
        headerRow.setFontWeight('bold');

        // Freeze the header row
        sheet.setFrozenRows(1);

        // Auto resize columns A - M
        sheet.autoResizeColumns(1, 13);
    }

    function formatColumnA() {
        var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
        var numRows = sheet.getMaxRows();
        var columnA = sheet.getRange(FIRST_DATA_ROW, 1, numRows - 1, 1); // Start from row 2 to exclude the header
        var values = columnA.getValues();

        for (var i = 0; i < values.length; i++) {
            var cell = columnA.getCell(i + 1, 1);
            var value = values[i][0].toString().toLowerCase();
            var exchange = Object.keys(EXCHANGE_COLORS).find((key) =>
                value.endsWith(key)
            );

            if (exchange) {
                cell.setBackground(
                    EXCHANGE_COLORS[exchange].background
                ).setFontColor(EXCHANGE_COLORS[exchange].fontColor);

                if (EXCHANGE_COLORS[exchange].fontWeight) {
                    cell.setFontWeight(EXCHANGE_COLORS[exchange].fontWeight);
                }
            }
        }
    }

    function formatDateTimeColumns() {
        var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
        var numRows = sheet.getMaxRows();

        DATE_COLUMNS.forEach(function (col) {
            var column = sheet.getRange(1, col, numRows, 1);
            column.setNumberFormat('M/d/yyyy H:mm:ss');
        });
    }

    function formatColumnD() {
        var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
        var numRows = sheet.getMaxRows();
        var columnD = sheet.getRange(2, 4, numRows - 1, 1); // Start from row 2 to exclude the header
        var values = columnD.getValues();

        for (var i = 0; i < values.length; i++) {
            var cell = columnD.getCell(i + 1, 1);
            var value = values[i][0].toString().toLowerCase();

            if (value === 'buy') {
                cell.setBackground(CELL_COLORS.buy);
            } else if (value === 'sell') {
                cell.setBackground(CELL_COLORS.sell);
            }
        }
    }

    function formatColumnE() {
        var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
        var numRows = sheet.getMaxRows();
        var columnE = sheet.getRange(2, 5, numRows - 1, 1); // Start from row 2 to exclude the header
        var customNumberFormat = '0.00000000'; // Custom number format with a precision of 1 * 10 ^ -8

        columnE.setNumberFormat(customNumberFormat);
    }

    function formatCurrencyColumns() {
        var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
        var numRows = sheet.getMaxRows();

        // Format Columns F, G, H, and I
        var currencyColumns1 = sheet.getRange(2, 6, numRows - 1, 4); // Start from row 2 to exclude the header
        currencyColumns1.setNumberFormat('$0.00');

        // Format Columns K and L
        var currencyColumns2 = sheet.getRange(2, 11, numRows - 1, 2); // Start from row 2 to exclude the header
        currencyColumns2.setNumberFormat('$0.00');
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
                cell.setBackground('#fce8b2');
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
                cell.setBackground('#b7e1cd');
            } else if (value < 0) {
                cell.setBackground('#f4c7c3');
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
                cell.setBackground('#fce8b2');
            }
        }
    }

    leftAlignColumns();
    centerAlignColumns();
    rightAlignColumns();
    formatHeaderRow();
    formatColumnA();
    formatDateTimeColumns();
    formatColumnD();
    formatColumnE();
    formatCurrencyColumns();
    formatColumnK();
    formatColumnL();
    formatColumnM();
}

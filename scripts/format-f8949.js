const CELL_COLORS = {
    buy: "#b7e1cd",
    sell: "#f4c7c3",
    highlight: "#fce8b2",
};

const EXCHANGE_COLORS = {
    robinhood: { background: "#38761d", fontColor: "white" },
    coinbase: { background: "#1155cc", fontColor: "white" },
    coinbase_pro: { background: "#434343", fontColor: "white" },
    kraken: { background: "#674ea7", fontColor: "white" },
    total: { background: "#fce8b2", fontColor: "black", fontWeight: "bold" },
};

function formatForm8949() {
    const LEFT_ALIGNED_COLUMNS = [1, 2, 3];
    const RIGHT_ALIGNED_COLUMN_PAIRS = [
        { start: 4, count: 2 },
        { start: 7, count: 2 },
    ];
    const CURRENCY_COLUMNS = [4, 5, 7, 8];
    const DATE_COLUMNS = [2, 3];
    const HEADER_ROW = 1;
    const FIRST_DATA_ROW = HEADER_ROW + 1;

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    // Get the number of rows and columns in the sheet
    var numRows = sheet.getMaxRows();
    var numColumns = sheet.getMaxColumns();

    function leftAlignColumns() {
        LEFT_ALIGNED_COLUMNS.forEach(function (column) {
            var range = sheet.getRange(HEADER_ROW, column, numRows, 1);
            range.setHorizontalAlignment("left");
        });
    }

    function rightAlignColumns() {
        RIGHT_ALIGNED_COLUMN_PAIRS.forEach(function (pair) {
            var range = sheet.getRange(
                HEADER_ROW,
                pair.start,
                numRows,
                pair.count
            );
            range.setHorizontalAlignment("right");
        });
    }

    function formatHeaderRow() {
        // Center align the header row
        var headerRow = sheet.getRange(1, 1, 1, numColumns);
        headerRow.setHorizontalAlignment("center");

        // Make the header row bold
        headerRow.setFontWeight("bold");

        // Freeze the header row
        sheet.setFrozenRows(1);

        // Auto resize columns A - H
        sheet.autoResizeColumns(1, 8);
    }

    function insertTotalValues() {
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
        // Start from row 2 to exclude the header
        var columnA = sheet.getRange(FIRST_DATA_ROW, 1, numRows - 1, 1);
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

    function formatDateColumns() {
        DATE_COLUMNS.forEach(function (column) {
            // Start from row 2 to exclude the header
            var range = sheet.getRange(FIRST_DATA_ROW, column, numRows - 1, 1);
            range.setNumberFormat("M/d/yyyy");
        });
    }

    function formatCurrencyColumns() {
        CURRENCY_COLUMNS.forEach(function (column) {
            // Start from row 2 to exclude the header
            var range = sheet.getRange(FIRST_DATA_ROW, column, numRows - 1, 1);
            range.setNumberFormat("$#,##0.00");
        });
    }

    function formatColumnH() {
        var columnH = sheet.getRange(FIRST_DATA_ROW, 8, numRows - 1, 1);
        var values = columnH.getValues();

        for (var i = 0; i < values.length; i++) {
            var cell = columnH.getCell(i + 1, 1);
            var value = values[i][0];

            if (value === "" || value === null) {
                continue;
            } else if (value > 0) {
                cell.setBackground(CELL_COLORS.buy);
            } else if (value < 0) {
                cell.setBackground(CELL_COLORS.sell);
            } else {
                cell.setBackground(CELL_COLORS.highlight);
            }
        }
    }

    leftAlignColumns();
    rightAlignColumns();
    formatHeaderRow();
    insertTotalValues();
    formatColumnA();
    formatDateColumns();
    formatCurrencyColumns();
    formatColumnH();
}

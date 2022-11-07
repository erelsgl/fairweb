import gspread

account = gspread.service_account("credentials.json")
spreadsheet = account.open("TestSpreadsheet")
sheet1 = spreadsheet.worksheet("Sheet1")
print("Rows: ", sheet1.row_count, "Cols: ", sheet1.col_count)
print("gspread OK!")

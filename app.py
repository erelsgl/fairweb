import gspread
import fairpy

account = gspread.service_account("credentials.json")
spreadsheet = account.open("FairDivision")
input = spreadsheet.worksheet("input")
print("Rows: ", input.row_count, "Cols: ", input.col_count)
rows = input.get_all_values()
print(rows)
items = rows[0][2:]
print("items: ", items)
rows_of_agents = rows[1:-1]    # remove heading and summary
agents = [row[0] for row in rows_of_agents]         
print("agents: ", agents)
entitlements = [row[1] for row in rows_of_agents]   # remove heading and summary
print("entitlements: ", entitlements)
preferences = {row[0]: row[2:] for row in rows_of_agents}
print("preferences: ",preferences)

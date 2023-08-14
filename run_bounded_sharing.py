import gspread
from bounded_sharing import input, allocate, output

def run(url:str, language:str="he"):
    print("\nOPENING SPREADSHEET")
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)

    print("\nREADING INPUT DATA")
    rows = input.read_rows(spreadsheet)
    agents, items, entitlement_normalized_preferences  = input.analyze_rows(rows)
    print("agents: ", agents, "items: ", items)

    print("\nCOMPUTING ALLOCATION")
    map_agent_to_fractions = allocate.allocate(agents, entitlement_normalized_preferences)
    print("allocation: ", map_agent_to_fractions)

    print("\nUPDATING OUTPUT SHEET")
    new_row_count = len(agents)+2
    new_col_count = len(items)+5
    output_sheet = output.worksheet(spreadsheet, new_row_count, new_col_count)
    output_sheet.clear()
    new_cells = output.cells(rows, agents, items, map_agent_to_fractions, language)
    output_sheet.update_cells(new_cells, value_input_option='USER_ENTERED')

    print("\nFORMATTING OUTPUT SHEET")
    first_cell = gspread.utils.rowcol_to_a1(2, 3)
    last_cell = gspread.utils.rowcol_to_a1(len(agents)+2, len(items)+5)
    output_sheet.format(f"{first_cell}:{last_cell}", {"numberFormat": {"type": "PERCENT", "pattern": "##.#%"}})

if __name__=="__main__":
    URL_FOR_GOVERNMENT = "https://docs.google.com/spreadsheets/d/1tJPV-y-r1TAx5FqbrqecKPJMeKHTtIDeiYck8eLoGKY"
    run(URL_FOR_GOVERNMENT)

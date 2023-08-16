import gspread
from courses import input, allocate, output
from gspread_utils import get_or_create_worksheet
from fairpy.courses import divide

def run(url:str, language:str="he"):
    print("\nOPENING SPREADSHEET")
    account = gspread.service_account("credentials.json")
    spreadsheet = account.open_by_url(url)

    print("\nREADING INPUT DATA")
    rows = input.read_rows(spreadsheet)
    agent_capacities, item_capacities, valuations  = input.analyze_rows(rows)
    print("agent_capacities: ", agent_capacities, "item_capacities: ", item_capacities)

    print("\nCOMPUTING ALLOCATION")
    map_agent_to_bundle, map_agent_to_explanation = allocate.allocate(agent_capacities, item_capacities, valuations)
    print("allocation: ", map_agent_to_bundle)

    print("\nUPDATING OUTPUT SHEET")
    new_row_count = len(agent_capacities)+2
    new_col_count = len(item_capacities)+5
    output_sheet = get_or_create_worksheet(spreadsheet, ["allocation", "חלוקה"], new_row_count, new_col_count)
    output_sheet.clear()
    new_cells = output.cells(rows, agent_capacities, item_capacities, map_agent_to_bundle, map_agent_to_explanation, language)
    output_sheet.update_cells(new_cells, value_input_option='USER_ENTERED')

    print("\nUPDATING EXPLANATION SHEETS")
    for agent,explanation in map_agent_to_explanation.items():
        agent_explanation_sheet = get_or_create_worksheet(spreadsheet, [agent], 1, 1)
        agent_explanation_sheet.clear()
        print(agent, ": ", explanation)
        agent_explanation_sheet.update_cell(1, 1, explanation)

    # print("\nFORMATTING OUTPUT SHEET")
    # first_cell = gspread.utils.rowcol_to_a1(2, 3)
    # last_cell = gspread.utils.rowcol_to_a1(len(agent_capacities)+2, len(item_capacities)+5)
    # output_sheet.format(f"{first_cell}:{last_cell}", {"numberFormat": {"type": "PERCENT", "pattern": "##.#%"}})

if __name__=="__main__":
    from courses.example_url import EXAMPLE_URL
    run(EXAMPLE_URL)

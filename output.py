"""
Utilities for updating the output spreadsheet.
"""

import gspread
import logging
from gspread_utils import get_worksheet_by_list_of_possible_names



logger = logging.getLogger(__name__)

TEXTS = {
	"value_percent": {
		"he": "ערך באחוזים",
		"en": "Value in percent",
	},
	"due_value_percent": {
		"he": "ערך מגיע באחוזים",
		"en": "Due value in percent",
	},
	"value_ratio": {
		"he": "יחס ערכים",
		"en": "Value ratio",
	},
}


def worksheet(spreadsheet:gspread.Spreadsheet, new_row_count,  new_col_count)->gspread.Worksheet:
	output_sheet = get_worksheet_by_list_of_possible_names(spreadsheet, ["תוצאות", "output"])
	if output_sheet is not None:
		if output_sheet.row_count < new_row_count:
			output_sheet.add_rows(new_row_count - output_sheet.row_count)
		if output_sheet.col_count < new_col_count:
			output_sheet.add_cols(new_col_count - output_sheet.col_count)
	else: # if output_sheet is None:
		output_sheet = spreadsheet.add_worksheet(title="output", rows=new_row_count, cols=new_col_count)
		# TODO: change worksheet direction to RTL
		# I did not find here https://docs.gspread.org/en/latest/api/models/worksheet.html#id1   how to do this.
	# input_range = input.range(1, 1, len(rows), len(rows[0]))
	# output.update_cells(input_range)
	return output_sheet

def cells(input_rows, agents, items, map_agent_to_fractions, language="he"):
	"""
	Returns new cells, for updating the output worksheet.
	"""

	def text(code:str):
		return TEXTS[code][language]

	NAME_COLUMN = 1
	ENTITLEMENT_COLUMN = 2

	new_cells = []
	new_cells += [gspread.Cell(i+1, NAME_COLUMN, "=input!"+gspread.utils.rowcol_to_a1(i+1,1)) for i in range(len(input_rows))]  # Copy column 1
	new_cells += [gspread.Cell(i+1, ENTITLEMENT_COLUMN, "=input!"+gspread.utils.rowcol_to_a1(i+1,2)) for i in range(len(input_rows))]  # Copy column 2
	new_cells += [gspread.Cell(1, o+3, items[o]) for o in range(len(items))]   # Write item names

	# Insert results:
	for i in range(len(agents)):
		bundle_i = map_agent_to_fractions[agents[i]]
		print(agents[i], ": ", bundle_i)
		for o in range(len(items)):
			fraction_i_o = map_agent_to_fractions[agents[i]][o]
			new_cells += [gspread.Cell(i+2, o+3, fraction_i_o)]

	row_of_total = len(agents)+2
	for o in range(len(items)):
		col = o+3
		first_cell = gspread.utils.rowcol_to_a1(2, col)
		last_cell = gspread.utils.rowcol_to_a1(len(agents)+1, col)
		new_cells += [gspread.Cell(row_of_total, col, f"=SUM({first_cell}:{last_cell})")]

	# Insert formula for computing the utilities:

	utility_column = len(items)+4
	new_cells += [gspread.Cell(1, utility_column,  text("value_percent"))]
	new_cells += [gspread.Cell(1, utility_column+1, text("due_value_percent"))]
	new_cells += [gspread.Cell(1, utility_column+2, text("value_ratio"))]

	for i in range(len(agents)):
		row_num = i+2
		first_cell = gspread.utils.rowcol_to_a1(row_num, 3)
		last_cell = gspread.utils.rowcol_to_a1(row_num, len(items)+2)
		range_a1 = f"{first_cell}:{last_cell}"
		new_cells += [gspread.Cell(row_num, utility_column, f"=SUMPRODUCT(input!{range_a1},output!{range_a1})/sum(input!{range_a1})")]

		utility_cell = gspread.utils.rowcol_to_a1(row_num, utility_column)
		entitlement_cell = gspread.utils.rowcol_to_a1(row_num, ENTITLEMENT_COLUMN)
		first_entitlement_cell = gspread.utils.rowcol_to_a1(2, ENTITLEMENT_COLUMN)
		last_entitlement_cell = gspread.utils.rowcol_to_a1(len(agents)+1, ENTITLEMENT_COLUMN)
		new_cells += [gspread.Cell(row_num, utility_column+1, f"={entitlement_cell}/SUM({first_entitlement_cell}:{last_entitlement_cell})")]

		entitlement_cell_percent = gspread.utils.rowcol_to_a1(row_num, utility_column+1)
		new_cells += [gspread.Cell(row_num, utility_column+2, f"={utility_cell}/{entitlement_cell_percent}")]

	return new_cells

# print("output version 2")
	
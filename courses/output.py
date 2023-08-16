"""
Utilities for updating the output spreadsheet.
"""

import gspread
import logging, sys, os

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 
from gspread_utils import get_worksheet_by_list_of_possible_names



logger = logging.getLogger(__name__)

TEXTS = {
	"intro": {
		"he": "גליון זה הוא הפלט של אלגוריתם החלוקה. ",
		"en": "This is the output of the fair allocation algorithm."
	},
	"agent_name": {
		"he": "סטודנט v",
		"en": "student v"
	},
	"item_name": {
		"he": "קורס >",
		"en": "course >"
	},
	"capacity": {
		"he": "מקס' מקומות",
		"en": "capacity",
	},
	"seats": {
		"he": "מקומות בפועל",
		"en": "seats",
	},
}

def cells(input_rows, agent_capacities, item_capacities, map_agent_to_bundle, map_agent_to_explanation, language="he"):
	"""
	Returns new cells, for updating the output worksheet.
	"""

	def text(code:str):
		return TEXTS[code][language]

	AGENT_NAME_COLUMN     = 1
	AGENT_CAPACITY_COLUMN = 2
	AGENT_BUNDLE_COLUMN   = 4
	INTRO_ROW = 1
	ITEM_NAME_ROW = 2
	ITEM_CAPACITY_ROW = 3

	new_cells = []
	agents = list(agent_capacities.keys())
	items  = list(item_capacities.keys())
	new_cells += [gspread.Cell(INTRO_ROW,  1,text("intro"))]
	new_cells += [gspread.Cell(INTRO_ROW+1,2,text("item_name"))]
	new_cells += [gspread.Cell(INTRO_ROW+2,1,text("agent_name"))]
	new_cells += [gspread.Cell(INTRO_ROW+2,2,text("capacity"))]
	new_cells += [gspread.Cell(INTRO_ROW+3,3,text("seats"))]
	# new_cells += [gspread.Cell(i+1, AGENT_NAME_COLUMN, "=valuations!"+gspread.utils.rowcol_to_a1(i+1,AGENT_NAME_COLUMN)) for i in range(len(input_rows))]     # Copy column 1: agent names
	# new_cells += [gspread.Cell(i+1, AGENT_CAPACITY_COLUMN, "=valuations!"+gspread.utils.rowcol_to_a1(i+1,AGENT_CAPACITY_COLUMN)) for i in range(len(input_rows))]  # Copy column 2: agent capacities
	# new_cells += [gspread.Cell(ITEM_NAME_ROW, o+3, items[o]) for o in range(len(items))]   # Write item names
	# new_cells += [gspread.Cell(ITEM_CAPACITY_ROW, o+3, items[o]) for o in range(len(items))]   # Write item names

	for o in range(len(items)):
		item_o = items[o]
		column = o+5
		column_letter = gspread.utils.rowcol_to_a1(1, column)[:-1]
		new_cells += [gspread.Cell(ITEM_NAME_ROW, column, item_o)]
		new_cells += [gspread.Cell(ITEM_NAME_ROW+1, column, item_capacities[item_o])]
		new_cells += [gspread.Cell(ITEM_NAME_ROW+2, column, f"=sum({column_letter}{ITEM_NAME_ROW+3}:{column_letter})")]

	# Insert results:
	for i in range(len(agents)):
		agent_i = agents[i]
		bundle_i = map_agent_to_bundle[agent_i]
		explanation_i = map_agent_to_explanation[agent_i]
		row = i+5
		print(agent_i, ": ", bundle_i)
		new_cells += [gspread.Cell(row, AGENT_NAME_COLUMN, agent_i)]
		new_cells += [gspread.Cell(row, AGENT_CAPACITY_COLUMN, agent_capacities[agent_i])]
		column_letter = gspread.utils.rowcol_to_a1(1, AGENT_CAPACITY_COLUMN+2)[:-1]
		new_cells += [gspread.Cell(row, AGENT_CAPACITY_COLUMN+1, f"=sum({column_letter}{row}:{row})")]
		new_cells += [gspread.Cell(row, AGENT_BUNDLE_COLUMN,   str(bundle_i))]
		for o in range(len(items)):
			item_o = items[o]
			column = o+5
			fraction_i_o = 1 if item_o in bundle_i else 0
			new_cells += [gspread.Cell(row, column, fraction_i_o)]

	# row_of_total = len(agents)+2
	# for o in range(len(items)):
	# 	col = o+3
	# 	first_cell = gspread.utils.rowcol_to_a1(2, col)
	# 	last_cell = gspread.utils.rowcol_to_a1(len(agents)+1, col)
	# 	new_cells += [gspread.Cell(row_of_total, col, f"=SUM({first_cell}:{last_cell})")]

	# # Insert formula for computing the utilities:

	# utility_column = len(items)+4
	# new_cells += [gspread.Cell(1, utility_column,  text("value_percent"))]
	# new_cells += [gspread.Cell(1, utility_column+1, text("due_value_percent"))]
	# new_cells += [gspread.Cell(1, utility_column+2, text("value_ratio"))]

	# for i in range(len(agents)):
	# 	row_num = i+2
	# 	first_cell = gspread.utils.rowcol_to_a1(row_num, 3)
	# 	last_cell = gspread.utils.rowcol_to_a1(row_num, len(items)+2)
	# 	range_a1 = f"{first_cell}:{last_cell}"
	# 	new_cells += [gspread.Cell(row_num, utility_column, f"=SUMPRODUCT(input!{range_a1},output!{range_a1})/sum(input!{range_a1})")]

	# 	utility_cell = gspread.utils.rowcol_to_a1(row_num, utility_column)
	# 	entitlement_cell = gspread.utils.rowcol_to_a1(row_num, ENTITLEMENT_COLUMN)
	# 	first_entitlement_cell = gspread.utils.rowcol_to_a1(2, ENTITLEMENT_COLUMN)
	# 	last_entitlement_cell = gspread.utils.rowcol_to_a1(len(agents)+1, ENTITLEMENT_COLUMN)
	# 	new_cells += [gspread.Cell(row_num, utility_column+1, f"={entitlement_cell}/SUM({first_entitlement_cell}:{last_entitlement_cell})")]

	# 	entitlement_cell_percent = gspread.utils.rowcol_to_a1(row_num, utility_column+1)
	# 	new_cells += [gspread.Cell(row_num, utility_column+2, f"={utility_cell}/{entitlement_cell_percent}")]

	return new_cells



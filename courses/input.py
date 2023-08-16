"""
Utilities for reading and analyzing the input from the spreadsheet.
"""

import gspread
import numpy as np
import logging, sys, os

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from gspread_utils import get_worksheet_by_list_of_possible_names

logger = logging.getLogger(__name__)


def read_rows(spreadsheet:gspread.Spreadsheet)->list[list[str]]:
	"""
	Returns a list of rows in the "input" worksheet of the given spreadsheet.
	Each row is a list of string values.
	"""
	input_sheet = get_worksheet_by_list_of_possible_names(spreadsheet, ["הערכות", "valuations"], error_if_not_found=True)
	logger.info("Rows: %d, Cols: %d", input_sheet.row_count, input_sheet.col_count)
	rows = input_sheet.get_all_values()
	return rows


def analyze_rows(rows:list[list[str]])->tuple[dict,dict,dict]:
	"""
	Analyzes the given list of rows. 
	Computes the inputs to fair course allocation algorithms:
	 * agent_capacities;
	 * item_capacities;
	 * valuations. The valuations are normalized to a fixed sum (1000).

	>>> rows = [['intro'], ['', 'item', 'total', 'c1', 'c2', 'c3', 'c4'], ['agent', 'capacity', '340', '40', '40', '40', '20'], ['s1', '6', '1000', '64', '34', '167', '132'], ['s2', '4', '1000', '105', '52', '179', '32'], ['s3', '4', '1000', '71', '164', '129', '100'], ['s4', '6', '1000', '21', '26', '161', '4'], ['s5', '3', '1000', '171', '115', '4', '157']]
	>>> agent_capacities, item_capacities, valuations = analyze_rows(rows)
	>>> agent_capacities
	{'s1': 6, 's2': 4, 's3': 4, 's4': 6, 's5': 3}
	>>> item_capacities
	{'c1': 40, 'c2': 40, 'c3': 40, 'c4': 20}
	>>> valuations
	{'s1': {'c1': 161, 'c2': 85, 'c3': 420, 'c4': 332}, 's2': {'c1': 285, 'c2': 141, 'c3': 486, 'c4': 86}, 's3': {'c1': 153, 'c2': 353, 'c3': 278, 'c4': 215}, 's4': {'c1': 99, 'c2': 122, 'c3': 759, 'c4': 18}, 's5': {'c1': 382, 'c2': 257, 'c3': 8, 'c4': 351}}
	"""
	ROW_OF_ITEM_NAMES = 1         # The item names are on row 1 (row 0 is for instructions).
	FIRST_COL_OF_ITEM_NAMES = 3   # The item names start at column 3 (columns 0,1,2 are for student names and capacities).
	items = rows[ROW_OF_ITEM_NAMES][FIRST_COL_OF_ITEM_NAMES:]
	items = [item for item in items if item != '']
	logger.info("items: %s", items)

	item_capacities = rows[ROW_OF_ITEM_NAMES+1][FIRST_COL_OF_ITEM_NAMES:]
	map_item_to_capacity = {items[i]: int(item_capacities[i]) for i in range(len(items))}
	logger.info("item_capacities: %s", map_item_to_capacity)

	FIRST_ROW_OF_AGENT_NAMES = 3                          # remove item names 
	rows_of_agents = rows[FIRST_ROW_OF_AGENT_NAMES:]  
	agents = [row[0] for row in rows_of_agents]         
	logger.info("agents: %s", agents)

	agent_capacities = [int(row[1]) for row in rows_of_agents]
	map_agent_to_capacity = {agents[i]: int(agent_capacities[i]) for i in range(len(agents))}
	logger.info("agent_capacities: %s", map_agent_to_capacity)

	def print_prefs(title, map_agent_to_prefs):
		logger.info(title)
		for agent,prefs in map_agent_to_prefs.items():
			logger.info("\t%s:\t\t%s\t\t%f",agent, prefs, sum(prefs.values()))	

	def row_to_prefs(row:list)->list:
		prefs_list = row[FIRST_COL_OF_ITEM_NAMES:]
		prefs_dict = {}
		for o in range(len(items)):
			value = prefs_list[o]
			value = 0.0 if value=='' else float(value)
			prefs_dict[items[o]] = value
		return prefs_dict
	raw_preferences = {row[0]: row_to_prefs(row) for row in rows_of_agents}
	print_prefs("raw valuations: ", raw_preferences)

	def normalized_prefs(prefs, new_sum):
		current_sum = sum(prefs.values())
		ratio = new_sum/current_sum
		return {item: int(value*ratio) for item,value in prefs.items()}

	# normalized_preferences = {
	# 	agent: normalized_prefs(prefs, total_entitlements) for agent,prefs in raw_preferences.items()
	# }
	# print_prefs("normalized_preferences: ", normalized_preferences)

	FIXED_SUM = 1000
	normalized_valuations = {
		agent: normalized_prefs(prefs, new_sum=FIXED_SUM) for agent,prefs in raw_preferences.items()
	}
	print_prefs("normalized valuations: ", normalized_valuations)
	return map_agent_to_capacity, map_item_to_capacity, normalized_valuations


if __name__=="__main__":
	logger.addHandler(logging.StreamHandler())
	# logger.setLevel(logging.INFO)

	import doctest
	print(doctest.testmod(optionflags=doctest.ELLIPSIS))

	# from example_url import EXAMPLE_URL
	# account = gspread.service_account("../credentials.json")
	# spreadsheet = account.open_by_url(EXAMPLE_URL)
	# rows = read_rows(spreadsheet)
	# print(rows)
	# analyze_rows(rows)

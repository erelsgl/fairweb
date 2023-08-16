"""
Utilities for reading and analyzing the input from the spreadsheet.
"""

import gspread
from typing import *
import numpy as np
import logging, sys, os

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from gspread_utils import get_worksheet_by_list_of_possible_names

logger = logging.getLogger(__name__)


def read_rows(spreadsheet:gspread.Spreadsheet)->List[List[str]]:
	"""
	Returns a list of rows in the "input" worksheet of the given spreadsheet.
	Each row is a list of string values.
	"""
	input_sheet = get_worksheet_by_list_of_possible_names(spreadsheet, ["נתונים", "input"], error_if_not_found=True)
	logger.info("Rows: %d, Cols: %d", input_sheet.row_count, input_sheet.col_count)
	rows = input_sheet.get_all_values()
	return rows


def analyze_rows(rows:List[List[str]])->Tuple[list,list,dict]:
	"""
	Analyzes the given list of rows. 
	Computes the list of agents, the list of items, and the dict mapping agents to their valuations.
	The valuations are normalized based on the entitlements.

	>>> rows = [['party', 'mandates', 'foreign', 'defence', 'finance', 'police', 'justice', 'interior', 'health', 'educations', '', 'total'], ['likkud', '32', '20', '20', '20', '10', '10', '10', '10', '20', '', '120'], ['religious', '14', '10', '20', '10', '30', '20', '10', '20', '20', '', '140'], ['shas', '11', '5', '5', '20', '5', '10', '30', '20', '20', '', '115'], ['aguda', '7', '5', '5', '5', '5', '5', '10', '20', '20', '', '75'], ['total', '64', '', '', '', '', '', '', '', '', '', '']]
	>>> agents, items, entitlement_normalized_preferences = analyze_rows(rows)
	>>> agents
	['likkud', 'religious', 'shas', 'aguda']
	>>> items
	['foreign', 'defence', 'finance', 'police', 'justice', 'interior', 'health', 'educations']
	>>> entitlement_normalized_preferences[agents[0]]
	{'foreign': 0.333, 'defence': 0.333, 'finance': 0.333, 'police': 0.167, 'justice': 0.167, 'interior': 0.167, 'health': 0.167, 'educations': 0.333}

	# Set entitlement to 0
	>>> rows = [['party', 'mandates', 'foreign', 'defence', 'finance', 'police', 'justice', 'interior', 'health', 'educations', '', 'total'], ['likkud', '0', '20', '20', '20', '10', '10', '10', '10', '20', '', '120'], ['religious', '14', '10', '20', '10', '30', '20', '10', '20', '20', '', '140'], ['shas', '11', '5', '5', '20', '5', '10', '30', '20', '20', '', '115'], ['aguda', '7', '5', '5', '5', '5', '5', '10', '20', '20', '', '75'], ['total', '64', '', '', '', '', '', '', '', '', '', '']]
	>>> agents, items, entitlement_normalized_preferences = analyze_rows(rows)
	>>> agents
	['likkud', 'religious', 'shas', 'aguda']
	>>> items
	['foreign', 'defence', 'finance', 'police', 'justice', 'interior', 'health', 'educations']
	>>> entitlement_normalized_preferences[agents[0]]  # doctest: +ELLIPSIS
	{'foreign': 5333.333, 'defence': 5333.333, 'finance': 5333.333, 'police': 2666.667, 'justice': 2666.667, 'interior': 2666.667, 'health': 2666.667, 'educations': 5333.333}
	"""
	ROW_OF_ITEM_NAMES = 0         # The item names are on row 0
	FIRST_COL_OF_ITEM_NAMES = 2   # The item names start at column 2 (columns 0,1 are for agent names, entitlements).
	items = rows[ROW_OF_ITEM_NAMES][FIRST_COL_OF_ITEM_NAMES:-1]  # remove last column (total)
	items = [item for item in items if item != '']
	logger.info("items: %s", items)


	FIRST_ROW_OF_AGENT_NAMES = 1                          # remove item names 
	rows_of_agents = rows[FIRST_ROW_OF_AGENT_NAMES:-1]    # remove total
	agents = [row[0] for row in rows_of_agents]         
	logger.info("agents: %s", agents)

	entitlements = [int(row[1]) for row in rows_of_agents]
	total_entitlements = sum(entitlements)
	map_agent_to_entitlement = {agents[i]: entitlements[i] for i in range(len(agents))}
	logger.info("entitlements: %s, total: %f", map_agent_to_entitlement, total_entitlements)

	def print_prefs(title, map_agent_to_prefs):
		logger.info(title)
		for agent,prefs in map_agent_to_prefs.items():
			logger.info("\t%s:\t\t%s\t\t%f",agent, prefs, sum(prefs.values()))	

	def row_to_prefs(row:list)->list:
		prefs_list = row[FIRST_COL_OF_ITEM_NAMES:-1]   # Remove party name, party entitlement, and total
		prefs_dict = {}
		for o in range(len(items)):
			value = prefs_list[o]
			value = 0.0 if value=='' else float(value)
			prefs_dict[items[o]] = value
		return prefs_dict
	raw_preferences = {row[0]: row_to_prefs(row) for row in rows_of_agents}
	print_prefs("raw_preferences: ", raw_preferences)

	def normalized_prefs(prefs, new_sum):
		current_sum = sum(prefs.values())
		ratio = new_sum/current_sum
		return {item: np.round(value*ratio,3) for item,value in prefs.items()}

	# normalized_preferences = {
	# 	agent: normalized_prefs(prefs, total_entitlements) for agent,prefs in raw_preferences.items()
	# }
	# print_prefs("normalized_preferences: ", normalized_preferences)

	EPSILON =  0.001
	entitlement_normalized_preferences = {
		agent: normalized_prefs(prefs, total_entitlements / (map_agent_to_entitlement[agent]+EPSILON)) for agent,prefs in raw_preferences.items()
	}
	print_prefs("entitlement_normalized_preferences: ", entitlement_normalized_preferences)
	return agents, items, entitlement_normalized_preferences


if __name__=="__main__":
	# logger.addHandler(logging.StreamHandler())
	# logger.setLevel(logging.INFO)
	import doctest
	print(doctest.testmod(optionflags=doctest.ELLIPSIS))
	account = gspread.service_account("../credentials.json")
	
	from example_url import EXAMPLE_URL
	spreadsheet = account.open_by_url(EXAMPLE_URL)
	print(read_rows(spreadsheet))

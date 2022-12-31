import gspread

def get_worksheet_by_list_of_possible_names(spreadsheet:gspread.Spreadsheet, possible_names:list)->gspread.Worksheet:
	"""
	Searches the given spreadsheet for a worksheet with a name from the given list.
	If none is found, return None.
	"""
	worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
	for name in possible_names:
		if name in worksheet_names:
			return spreadsheet.worksheet(name)
	return None

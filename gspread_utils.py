import gspread

def get_worksheet_by_list_of_possible_names(spreadsheet:gspread.Spreadsheet, possible_names:list, error_if_not_found:bool=False)->gspread.Worksheet:
	"""
	Searches the given spreadsheet for a worksheet with a name from the given list.
	If none is found, return None.
	"""
	worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
	for name in possible_names:
		if name in worksheet_names:
			return spreadsheet.worksheet(name)
	if error_if_not_found:
		raise gspread.WorksheetNotFound(f"Did not find a worksheet with name in {possible_names}. Worksheets are: {worksheet_names}")
	return None

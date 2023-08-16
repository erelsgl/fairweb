import gspread

def get_worksheet_by_list_of_possible_names(spreadsheet:gspread.Spreadsheet, possible_names:list, error_if_not_found:bool=False)->gspread.Worksheet:
	"""
	Searches the given spreadsheet for a worksheet with a name from the given list.
	If none is found, return None or raise an Error.
	"""
	worksheet_names = [ws.title for ws in spreadsheet.worksheets()]
	for name in possible_names:
		if name in worksheet_names:
			return spreadsheet.worksheet(name)
	if error_if_not_found:
		raise gspread.WorksheetNotFound(f"Did not find a worksheet with name in {possible_names}. Worksheets are: {worksheet_names}")
	return None


def get_or_create_worksheet(spreadsheet:gspread.Spreadsheet, possible_names:list, new_row_count,  new_col_count)->gspread.Worksheet:
	"""
	Searches the given spreadsheet for a worksheet with a name from the given list.
	If none is found, creates a new one.
	If one is found, ensures that it has enough rows and columns.
	"""
	output_sheet = get_worksheet_by_list_of_possible_names(spreadsheet, possible_names, error_if_not_found=False)
	if output_sheet is not None:
		if output_sheet.row_count < new_row_count:
			output_sheet.add_rows(new_row_count - output_sheet.row_count)
		if output_sheet.col_count < new_col_count:
			output_sheet.add_cols(new_col_count - output_sheet.col_count)
	else: # if output_sheet is None:
		default_name = possible_names[0]
		output_sheet = spreadsheet.add_worksheet(title=default_name, rows=new_row_count, cols=new_col_count)
		# TODO: change worksheet direction to RTL
		# I did not find here https://docs.gspread.org/en/latest/api/models/worksheet.html#id1   how to do this.
	# input_range = input.range(1, 1, len(rows), len(rows[0]))
	# output.update_cells(input_range)
	return output_sheet

def rows_to_stringdicts(rows):
	new_rows = [dict(zip(row.keys(), [str(x) for x in row])) for row in rows]
	return new_rows
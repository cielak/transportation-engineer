def all_cells(data):
    return all(all([cell != "" for cell in row.values()]) for row in data)

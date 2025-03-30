def pad_grid(grid_list):
    max_width = 0
    if not grid_list: return [] # grid_list could be np.array([]) which is False -> returns [] OK
    # What if grid_list is a numpy array?
    if isinstance(grid_list, np.ndarray):
         # Treat numpy array input directly? Or convert back to list?
         # Current code iterates row by row. This might work for np.ndarray.
         grid_list_processed = grid_list.tolist() # Safer to work with lists
    else:
         grid_list_processed = grid_list # Assume it's list-like

    # Check rows
    for row in grid_list_processed: # Iterating over rows of array works
        if isinstance(row, (list, tuple)): # Rows from .tolist() are lists
            max_width = max(max_width, len(row))
        # else: pass # This is problematic if a row isn't list/tuple

    padded_grid = []
    for row in grid_list_processed:
         if isinstance(row, (list, tuple)): # Should be true after .tolist()
            processed_row = []
            for x in row: # x should be elements from the original array
                try:
                    # If original array was object dtype, int(x) might fail
                    processed_row.append(int(x))
                except (ValueError, TypeError):
                    processed_row.append(0)
            padded_row = processed_row + [0] * (max_width - len(processed_row))
            padded_grid.append(padded_row)
         else:
            # This case might be hit if input wasn't list of lists or np.ndarray
            padded_grid.append([0] * max_width)

    return padded_grid
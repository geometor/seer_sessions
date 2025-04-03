    if isinstance(input_grid[0], list): # Handle potential [[...]] format
         grid_1d = np.array(input_grid[0])
    else:
         grid_1d = np.array(input_grid) # Assume already flat list
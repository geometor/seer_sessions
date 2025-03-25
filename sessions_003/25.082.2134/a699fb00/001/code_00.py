"""
Iterates through the input grid, identifies horizontally adjacent '1' (blue) pixels,
and inserts a '2' (red) pixel between them, shifting subsequent pixels on the row to the right.
"""

import numpy as np

def get_adjacent_horizontal(grid, r, c):
    """Returns the horizontally adjacent pixel's value and coordinates to the right, or None if it doesn't exist."""
    if c + 1 < len(grid[0]):
        return grid[r, c+1], r, c+1
    return None, None, None

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Initialize with a copy to retain dimensions and unchanged pixels
    rows, cols = input_grid.shape

    for r in range(rows):
        insertions = 0 # keep track of shift due to insertions on this row
        for c in range(cols):
            original_c = c - insertions # correct index based on previous shifts
            if original_c >= cols-1 :
                break; # prevent going out of bounds
                
            val = input_grid[r, original_c]            
            
            adjacent_val, adj_r, adj_c = get_adjacent_horizontal(input_grid, r, original_c)

            if val == 1 and adjacent_val == 1:
                # Shift elements to the right to make space for the new '2'
                
                for shift_c in reversed(range(original_c + 2, cols)):
                    output_grid[r, shift_c] = output_grid[r, shift_c-1]
                
                output_grid[r, original_c + 1] = 2
                insertions +=1

    return output_grid.tolist()
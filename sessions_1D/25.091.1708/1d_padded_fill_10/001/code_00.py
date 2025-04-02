"""
Fill rows to the right starting from the first non-white pixel.

1. Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Identify the single non-white color present in the input grid. Let this be the `fill_color`.
3. Iterate through each row of the input grid, from top to bottom (row index `r`).
4. For the current row `r`, scan from left to right (column index `c`) to find the first column `start_c` where the pixel color matches the `fill_color`.
5. If such a `start_c` is found for row `r`:
    a. Iterate through the columns of the output grid for row `r`, starting from `start_c` up to the last column.
    b. Set the color of each pixel in this range (`output_grid[r][c]` where `c >= start_c`) to the `fill_color`.
6. If no pixel matching the `fill_color` is found in the input row `r`, the corresponding output row `r` remains unchanged (all white).
7. After processing all rows, return the completed output grid.
"""

import numpy as np

def find_fill_color(grid):
    """Finds the first non-zero color in the grid."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    return 0 # Return background color if no non-zero color is found

def find_first_occurrence_index(row, color):
    """Finds the index of the first occurrence of a color in a row."""
    indices = np.where(row == color)[0]
    if len(indices) > 0:
        return indices[0]
    return None # Return None if color not found in the row

def transform(input_grid):
    """
    Transforms the input grid by filling rows to the right starting from the 
    first occurrence of the non-white color in that row.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with the same dimensions, filled with white (0)
    output_array = np.zeros_like(input_array)

    # Identify the fill color (the single non-white color in the input)
    fill_color = find_fill_color(input_array)
    
    # If the grid is all white or no fill color identified, return the white grid
    if fill_color == 0:
        return output_array.tolist()

    # Iterate through each row of the input grid
    for r in range(height):
        input_row = input_array[r, :]
        
        # Find the column index of the first occurrence of the fill color in the current row
        start_c = find_first_occurrence_index(input_row, fill_color)
        
        # If the fill color is found in this row
        if start_c is not None:
            # Fill the output row from the start column to the right edge with the fill color
            output_array[r, start_c:] = fill_color
        # Else: the row remains white (as initialized)

    # Convert the output numpy array back to a list of lists
    return output_array.tolist()

"""
1.  **Identify Landmark Row:** Find the row index where all pixels are yellow (color value 4). If no such row exists, return original grid.
2.  **Define Source Region:**
    *   The source region *starts* at the top of the grid (row 0).
    *   The source region *ends* two rows *below* the landmark row.
3.  **Define Destination Region:** The destination region starts two rows *below* the landmark row.
4.  **Copy and Paste:** Copy the entire source region. Paste this copied region into the destination region, starting at the destination start row.
5. **Clear Remaining Rows:** Set all rows after the pasted region to black (0).
6. **Handle Edge Cases:**
    *   If no landmark is found, return the original input.
    *   If copying goes out of output grid bounds, return the original input.
"""

import numpy as np

def find_landmark_row(grid, color):
    # Find a row that is entirely of the specified color.
    for i, row in enumerate(grid):
        if all(cell == color for cell in row):
            return i
    return None

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()

    # Find the landmark row (all yellow/4s)
    landmark_row_index = find_landmark_row(input_grid, 4)

    if landmark_row_index is None:
        return input_grid.tolist() # cant do it, return original

    # Define Source Region: now includes 2 rows below
    source_end_row = min(landmark_row_index + 3, input_grid.shape[0]) # Ensure we don't go out of bounds
    source_region = input_grid[0:source_end_row]

    # Calculate the destination start row (two rows below landmark row)
    destination_start_row = landmark_row_index + 2

    #check destination bounds
    if(destination_start_row + source_region.shape[0] > output_grid.shape[0]):
        return input_grid.tolist() # cant do it, return original

    # Paste the source region into the destination area in the output grid.
    output_grid[destination_start_row:destination_start_row + source_region.shape[0]] = source_region
    
    #clear all rows after pasting operation
    output_grid[destination_start_row+ source_region.shape[0]:] = 0

    return output_grid.tolist()
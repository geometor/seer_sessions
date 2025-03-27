"""
1.  **Find Divider:** Identify the horizontal row of '4' (yellow) pixels that completely separates the input grid.
2.  **Discard:** Ignore all pixels located *below* the identified divider.
3.  **Extract:** Focus solely on the portion of the grid *above* the divider line.
4.  **Substitute:** Within this extracted section, replace all instances of '7' (orange) with '3' (green).
5. **Rotate:** Rotate 90 degrees anti-clockwise the extracted section.
6.  **Output:** The rotated and color-substituted, upper section of the grid is the final output.
"""

import numpy as np

def find_divider_row(grid, divider_color=4):
    # Find the row index where the divider (all pixels are of divider_color) is located.
    for i, row in enumerate(grid):
        if np.all(row == divider_color):
            return i
    return -1  # Return -1 if no divider is found

def rotate_anti_clockwise(grid):
    # Rotate the grid 90 degrees anti-clockwise using NumPy.
   return np.rot90(grid, k=1).tolist()

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    grid = np.array(input_grid)
    
    # Find the row index of the divider.
    divider_row_index = find_divider_row(grid)
    
    # If no divider is found, return an appropriate response (e.g., empty grid or original grid).
    if divider_row_index == -1:
        return [] # Or some other error handling
    
    # Extract the upper section of the grid (above the divider).
    upper_section = grid[:divider_row_index]

    # Create a copy of the upper section to modify and use as the output.
    output_grid = np.copy(upper_section)

    # Replace all instances of '7' with '3' in the output grid.
    output_grid[output_grid == 7] = 3

    # Rotate the output_grid 90 degrees anti-clockwise
    output_grid = rotate_anti_clockwise(output_grid)

    return output_grid
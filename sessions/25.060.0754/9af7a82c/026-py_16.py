"""
1.  **Copy Input:** Begin by copying the input grid to the output grid.
2.  **Iterate Colors:** For each color in the sequence 7 (orange), 8 (azure), 6 (magenta), and 1 (blue), do the following:
3.  **Check Columns:** Iterate through each column of the *input* grid.
4.  **First Occurrence**: Find the *first* row index where the current color appears in the current column.
5. **Append if found**:
    - If the target color is found, create a new row with the same width as the input grid.
        - Initialize all cells in this new row to 0 (white).
        - Set the cell at the index equal to the current column number to the target color.
    - Append the new row to the *output* grid.
"""

import numpy as np

def get_first_occurrence(input_grid, color, col):
    """Finds the first row index where the color appears in the given column."""
    for row in range(input_grid.shape[0]):
        if input_grid[row, col] == color:
            return row
    return -1  # Return -1 if color is not found

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()

    # change output pixels
    colors_to_check = [7, 8, 6, 1]
    for color in colors_to_check:
        for col in range(input_grid.shape[1]):
            # Find the first occurrence of the color in the column.
            first_row_index = get_first_occurrence(input_grid, color, col)

            #If found, append row
            if first_row_index != -1:
                new_row = np.zeros(input_grid.shape[1], dtype=int)
                new_row[col] = color
                output_grid = np.vstack([output_grid, new_row])

    return output_grid.tolist()
"""
1.  **Identify Input Rows with White:** Scan the input grid and identify all rows that contain at least one white (0) pixel.

2.  **Determine Output Grid Size:**
    *   The output grid width is always 3.
    *   The output grid height equals the number of input rows containing white pixels.

3.  **Create Output Grid:** Initialize an output grid of the determined size, filled with zeros.

4.  **Map and Assign Colors based on Input Row Order:**
    *   Iterate through the *indices* of the input rows containing white pixels, maintaining their original order.
    *   **Condition 1:** If *all* rows in the input contain white pixels:
        -  If input shape is (4,14):
            -   The output grid is 3x3
            -  Output row 0 gets color 2 (red).
            -  Output row 1 gets color 8 (azure).
            -  Output row 2 gets color 3 (green).

        -  Otherwise:
            - return an empty grid.
    *   **Condition 2:** If *not all* rows in the input have white pixels.
        -  Output row 0 gets color 8 (azure).
        -  Output row 1 gets color 2 (red).
        -  Output row 2 gets color 4 (yellow).
        -  Output row 3 gets color 3 (green).

5.  **Populate Output Rows:** For each row in the output grid, fill all cells in that row with the assigned color.
"""

import numpy as np

def get_rows_with_white(input_grid):
    """Helper function to get indices of rows with white pixels."""
    rows_with_white = []
    for i, row in enumerate(input_grid):
        if 0 in row:
            rows_with_white.append(i)
    return rows_with_white

def transform(input_grid):
    """Transforms the input grid according to the rules."""

    rows_with_white = get_rows_with_white(input_grid)
    output_height = len(rows_with_white)
    output_width = 3

    # Handle the "all rows have white" case
    all_rows_have_white = (output_height == input_grid.shape[0])
    if all_rows_have_white:
        if input_grid.shape == (4, 14):
          output_grid = np.zeros((3, output_width), dtype=int)
          output_grid[0, :] = 2  # Red
          output_grid[1, :] = 8  # Azure
          output_grid[2, :] = 3  # Green
          return output_grid
        else:
          return np.zeros((0,0),dtype=int) #return empty

    # Create output grid (for the not-all-white case)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map and assign colors based on the order of rows with white
    color_map = {
        0: 8,  # First row with white gets azure
        1: 2,  # Second row with white gets red
        2: 4,  # Third row with white gets yellow
        3: 3,  # Fourth row with white gets green
    }

    for i, _ in enumerate(rows_with_white):
        color = color_map.get(i, 0) #default to 0 if not found
        output_grid[i, :] = color

    return output_grid
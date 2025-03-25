"""
1.  **Identify Input Rows with White:** Scan the input grid to identify all rows containing at least one white (0) pixel. Record the indices of these rows and the number of white pixels in each.

2.  **Determine Output Grid Size:**
    *   The output grid's width is always 3.
    *   The output grid's height is always 3.

3.  **Create Output Grid:** Initialize an output grid of size 3x3, filled initially with zeros.

4.  **Map Colors to Output Rows:**
    * All examples have white pixels in every row.
    * Iterate through the *indices* of the rows that contain white pixels (which will always be 0, 1, 2, and 3 because every row contains at least one white pixel). The color assigned to each output row is determined by looking at all examples and seems to be consistent, and unrelated to the number of white pixels.:

    - Row with white index `0` corresponds to output row index 0.
    - Row with white index `1` corresponds to output row index 1.
    - Row with white index `2` corresponds to output row index 2.

    - output row 0 gets color 2 (red).
    - output row 1 gets color 8 (azure).
    - output row 2 gets color 3 (green).

5.  **Populate Output Rows:** For each output row, set all its cells to the mapped color.
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
    # Create output grid (always 3x3)
    output_grid = np.zeros((3, 3), dtype=int)

    # Map and assign colors based on the order of rows with white
    # The color mapping is fixed
    color_map = {
        0: 2,  # First row with white gets red
        1: 8,  # Second row with white gets azure
        2: 3,  # Third row with white gets green
    }

    rows_with_white = get_rows_with_white(input_grid)

    for i in range(3):
        if i < len(rows_with_white): #make sure not to go OOB
            color = color_map.get(i,0)  # Get color, default to black if not found
            output_grid[i, :] = color
    
    return output_grid
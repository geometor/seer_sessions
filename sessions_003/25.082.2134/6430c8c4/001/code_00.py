"""
1.  **Identify Sections:** Divide the input grid into two sections based on the horizontal line of '4's (yellow).
2.  **Top Section Focus:** Disregard the lower section of the input grid.
3.  **Count Rows:** Count the number of rows on the top section.
4.  **Create Output Grid:** Create a new grid consisting of '0' (white), with the number of rows from step 3 and 4 columns.
5.  **Overlay Shape:** Create a shape by replacing orange '7' by green '3', for all '7' in top section, copy and paste the resulting shapes to same coordinates on the new output grid.
"""

import numpy as np

def get_top_section(grid):
    """Finds the row index of '4's and returns the grid section above it."""
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row):
            return grid[:i]
    return None  # Return None if no row of '4's is found

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Identify Sections and get the top one.
    top_section = get_top_section(input_grid)

    # If there isn't a top_section return the original grid.
    if top_section is None:
        return input_grid
    
    # 2. Top section focus and 3. Count Rows.
    rows = len(top_section)
    
    # 4. Create output grid with dimensions based on top section
    output_grid = np.zeros((rows, 4), dtype=int)

    # 5. Overlay Shape.
    for i in range(rows):
        for j in range(4):
          if top_section[i][j] == 7:
            output_grid[i][j] = 3

    return output_grid
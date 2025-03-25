```python
"""
1.  **Find Leftmost Yellow:** Locate the index of the leftmost column in the input grid that contains at least one yellow (4) pixel.
2.  **Find Blue Column:** Locate the index of a column that contains *only* blue (1) pixels.
3.  **Determine Subgrid Width:** Calculate the width of the subgrid. The subgrid starts at the leftmost yellow column. The width of the subgrid is the distance between the leftmost yellow column and the blue column.
4.  **Create Subgrid:** Extract a subgrid from the input. The subgrid has the same height as the input grid. The subgrid's columns start at the leftmost yellow column (inclusive) and span the number of columns calculated in the previous step.
5.  **Replace Colors:** Within the extracted subgrid, replace all yellow (4) pixels with azure (8) pixels.
6.  **Output:** Return the modified subgrid.
"""

import numpy as np

def find_leftmost_yellow_column(grid):
    """Finds the index of the leftmost column containing a yellow (4) pixel."""
    for j in range(grid.shape[1]):
        for i in range(grid.shape[0]):
            if grid[i, j] == 4:
                return j
    return -1  # Should not happen in valid input

def find_blue_column(grid):
    """Finds the index of the column containing ONLY blue (1) pixels."""
    for j in range(grid.shape[1]):
        column = grid[:, j]
        if np.all(column == 1):
            return j
    return -1

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the leftmost yellow column
    leftmost_yellow_column = find_leftmost_yellow_column(input_grid)

    # Find the blue column
    blue_column = find_blue_column(input_grid)

    # Determine subgrid width
    subgrid_width = blue_column - leftmost_yellow_column

    # Create subgrid
    output_grid = input_grid[:, leftmost_yellow_column:leftmost_yellow_column + subgrid_width].copy()

    # Replace yellow (4) with azure (8) within the subgrid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 4:
                output_grid[i, j] = 8

    return output_grid.tolist()
```
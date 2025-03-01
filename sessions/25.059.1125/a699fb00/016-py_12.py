"""
1.  **Identify Objects:**  Locate all blue pixels (value 1) within the input grid. These are the primary objects.
2.  **Check Adjacency:** For each blue pixel, examine its eight neighbors (including diagonals).
3.  **Conditional Transformation**:If a blue pixel is adjacent to at least one other *blue* pixel, then change its value to 2.
4. **Preserve Other Pixels:** All White pixels should remain white
5.  **Output:** Produce a new grid with the transformed values, maintaining the original dimensions.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 8 neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the cell itself
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels 
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 1:  # If it's a blue pixel
                neighbors = get_neighbors(input_grid, row, col)
                if 1 in neighbors:  # Check for adjacent blue pixels
                    output_grid[row, col] = 2  # Change to red

    return output_grid
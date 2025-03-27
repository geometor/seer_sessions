```python
"""
Transforms an input grid by replacing certain instances of the number 6 with the number 2,
based on the presence of neighboring 7s. A 6 is replaced by a 2 if and only if at least one of its eight neighbors (horizontal, vertical, and diagonal) in the input grid has a value of 7.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of neighboring cell values (including diagonals) for a given cell in a grid.
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the cell itself
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)  # Ensure it's a NumPy array
    output_grid = input_grid.copy()    # Initialize output_grid as a copy of input_grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the input_grid
    for row in range(rows):
        for col in range(cols):
            # Check the value in the input_grid
            if input_grid[row, col] == 6:
                # Check for neighboring 7s in the input_grid
                neighbors = get_neighbors(input_grid, row, col)
                if 7 in neighbors:
                    output_grid[row, col] = 2  # Replace 6 with 2 in output_grid

    return output_grid.tolist()  # Return as list of lists

```
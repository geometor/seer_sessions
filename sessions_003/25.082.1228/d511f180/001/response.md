```python
"""
1.  **Identify the second column** in the input grid.
2.  **Examine Input and Output:** Find any cells in column 2 of the Input grid that have a value that is the same as the values of its top or left neighbors in the Input grid.
3.  **For any cells identified**, change the value of the cell to the value of cell in Input grid, same row, last column.
4. **Copy** all other cells from the input grid to the output grid, maintaining their original values.
"""

import numpy as np

def get_neighbor_values(grid, row, col):
    """Gets the values of the top and left neighbors of a cell."""
    neighbors = {}
    if row > 0:
        neighbors['top'] = grid[row - 1, col]
    if col > 0:
        neighbors['left'] = grid[row, col - 1]
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    input_grid = np.array(input_grid)  # Use numpy for easier manipulation
    output_grid = np.copy(input_grid)  # Start with a copy
    rows, cols = input_grid.shape

    # Iterate through the second column (index 1)
    for row in range(rows):
        # second column
        col = 1
        
        # find neighbor values
        neighbor_values = get_neighbor_values(input_grid, row, col)

        # Check condition: If cell value == top or left neighbor
        if input_grid[row, col] == neighbor_values.get('top') or \
           input_grid[row, col] == neighbor_values.get('left'):
            
            # set to value of last column, same row
            output_grid[row, col] = input_grid[row, cols-1]

    return output_grid.tolist() # return regular python list
```
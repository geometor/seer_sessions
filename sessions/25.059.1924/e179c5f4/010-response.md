# e179c5f4 • 010 • refine_coder

---
```python
"""
The transformation rule consistently changes 0 to 8, but only in specific cases,
and leaves 1 unchanged. The key is to determine under what condition the 0
changes to 8, since non-0 and non-1 values remain unchanged. Looking at the
input, the changes from zero to eight only happen in example where the zero is
surrounded by the same numbers.

1.  Iterate through each cell of the input grid.
2.  Check if the cell's value is 0.
3.  If it is 0, check its immediate neighbors (up, down, left, right).
    *   If any adjacent cells have a different value (and are not 0 themselves
        since 0 changes to 8), do not change.
    *   If all adjacent neighbor cells have the same value, change cell to 8
4.  If not zero keep the cell's original value.
5.  Return the modified grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the values of the immediate neighbors (up, down, left, right) of a cell.
    Returns a list of neighbor values.  Handles edge cases by excluding
    out-of-bounds neighbors.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels based on neighbors
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                
                # Check if neighbors exist
                if not neighbors:  
                  continue
                
                # Check if the neighbors are the same
                first_neighbor = neighbors[0]
                all_same = all(neighbor == first_neighbor for neighbor in neighbors)

                if all_same:
                    output_grid[row,col] = 8
            # else, the value is preserved by np.copy

    return output_grid
```

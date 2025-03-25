```python
"""
Replace '7' (orange) with '5' (gray) on the edges of the grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing '7' (orange) with '5' (gray) on the edges.
    
    Args:
        input_grid (list of lists): The input grid.
    
    Returns:
        list of lists: The transformed grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = [row[:] for row in input_grid]  # Create a copy

    # Iterate through each cell
    for i in range(rows):
        for j in range(cols):
            # Check if the cell is on the edge and has color '7'
            if (i == 0 or i == rows - 1 or j == 0 or j == cols - 1) and input_grid[i][j] == 7:
                output_grid[i][j] = 5  # Change to '5' (gray)

    return output_grid
```

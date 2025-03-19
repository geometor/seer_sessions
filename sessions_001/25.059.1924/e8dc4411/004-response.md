# e8dc4411 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the source:** Locate the initial position (row, column) of the color '2' (red) within the input grid.
2.  **Replicate diagonally:** Starting from the row immediately below the source, and the column immediately to the right of the source, and continuing diagonally downwards and to the right, change the color of each cell to '2' (red).
3. **Termination:** Continue the diagonal replication until the edge of the grid is reached, either bottom or right.
4. **Preservation:** All other cells that do not fall under this rule remains the same, unless they are azure cells that happen to be in path of the diagonal of color '2'.
"""

import numpy as np

def find_color_position(grid, color):
    # Find the position of the first occurrence of a given color.
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == color:
                return (r, c)  # Return row and column
    return None  # Color not found


def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find the source position of color '2' (red).
    source_position = find_color_position(input_grid, 2)
    
    if source_position is None:  # Handle the case where color 2 is not found
        return output_grid
    
    row, col = source_position
    row += 1
    col += 1
    
    # Replicate '2' diagonally downwards and to the right.
    while row < output_grid.shape[0] and col < output_grid.shape[1]:
        output_grid[row, col] = 2
        row += 1
        col += 1
    
    return output_grid
```

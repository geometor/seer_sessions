```python
"""
Transforms a 3x3 input grid into a 3x3 output grid based on the position of '5's in the input. The output grid is filled row by row,
with each row's color determined by the presence of a '5' in specific positions within the input grid.

- Row 1: If '5' is at (0,0), the row is filled with '2'. If '5' is at (0,1), the row is filled with '4'. If '5' is at (0,2), the row is filled with '3'.
- Row 2: If '5' is at (1,1), the row is filled with '2'. If '5' is at (1,2), the row is filled with '3'.
- Row 3: If '5' is at (2,0), the row is filled with '3'. If '5' is at (2,1), the row is filled with '4'. If '5' is at (2,2), the row is filled with '2'.
"""

import numpy as np

def find_fives(grid):
    """Finds the positions of '5's in the grid."""
    five_positions = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 5:
                five_positions.append((r, c))
    return five_positions

def transform(input_grid):
    # Initialize output_grid with zeros
    output_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Find the positions of '5's
    five_positions = find_fives(input_grid)

    # Determine and fill Row 1
    if (0, 0) in five_positions:
        output_grid[0] = [2, 2, 2]
    if (0, 1) in five_positions:
        output_grid[0] = [4, 4, 4]
    if (0, 2) in five_positions:
        output_grid[0] = [3, 3, 3]

    # Determine and fill Row 2
    if (1, 1) in five_positions:
        output_grid[1] = [2, 2, 2]
    if (1, 2) in five_positions:
        output_grid[1] = [3, 3, 3]
        
    # Determine and fill Row 3
    if (2, 0) in five_positions:
        output_grid[2] = [3, 3, 3]
    if (2, 1) in five_positions:
        output_grid[2] = [4, 4, 4]
    if (2, 2) in five_positions:
        output_grid[2] = [2, 2, 2]

    return output_grid
```
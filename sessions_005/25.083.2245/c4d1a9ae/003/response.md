```python
"""
Transforms an input grid based on horizontal and vertical neighbor rules.

Horizontal Neighbor Rule (Same Color):
    - If a pixel has left and right neighbors of the same color:
        - If neighbors are 4 (yellow) and the current pixel is 4, change to 6 (magenta).
        - If neighbors are 0 (white) and the current pixel is 0, change to 3 (green).
        - If neighbors are 0 (white) and the current pixel is 4, change to 9 (maroon).

Vertical Neighbor Rule (Example 2 Specific):
    - If a pixel is 0 (white) and:
      -  the pixel above is 0 and the pixel below is NOT 0, change to 3
      - the pixel above is NOT 0 and the pixel below IS 0, change to 3
      -  the pixel above and the pixel below are both 0, change to 3.

No Change Rule:
    - If none of the above, pixel's value remains unchanged.
"""

import numpy as np

def get_horizontal_neighbors(grid, row, col):
    """Gets the immediate left and right neighbors of a pixel.
       Returns None for a neighbor if it's out of bounds.
    """
    rows, cols = grid.shape
    left_neighbor = grid[row, col - 1] if col > 0 else None
    right_neighbor = grid[row, col + 1] if col < cols - 1 else None
    return left_neighbor, right_neighbor

def get_vertical_neighbors(grid, row, col):
    """Gets the immediate top and bottom neighbors of a pixel.
       Returns None for a neighbor if it's out of bounds.
    """
    rows, cols = grid.shape
    top_neighbor = grid[row - 1, col] if row > 0 else None
    bottom_neighbor = grid[row + 1, col] if row < rows - 1 else None
    return top_neighbor, bottom_neighbor

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)  # Initialize output grid
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Get horizontal neighbors
            left_neighbor, right_neighbor = get_horizontal_neighbors(input_grid, row, col)

            # Horizontal Rule
            if left_neighbor is not None and right_neighbor is not None:
                if left_neighbor == right_neighbor:
                    if left_neighbor == 4 and output_grid[row, col] == 4:
                        output_grid[row, col] = 6
                    elif left_neighbor == 0 and output_grid[row, col] == 0:
                        output_grid[row, col] = 3
                    elif left_neighbor == 0 and output_grid[row, col] == 4:
                        output_grid[row, col] = 9

            # Vertical Rule
            top_neighbor, bottom_neighbor = get_vertical_neighbors(input_grid, row, col)
            if output_grid[row,col] == 0:  #current pixel has to be white.
                if top_neighbor == 0 and bottom_neighbor != 0:
                    output_grid[row,col] = 3
                elif top_neighbor != 0 and bottom_neighbor == 0:
                    output_grid[row,col] = 3
                elif top_neighbor == 0 and bottom_neighbor == 0:
                    output_grid[row,col] = 3


    return output_grid
```

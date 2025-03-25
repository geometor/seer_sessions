```python
"""
Transforms an input grid based on horizontal and vertical neighbor rules.

Horizontal Rules:
    1. If a pixel is 4 and both left and right neighbors are 4, change to 6.
    2. if current pixel is 4, and neighbors are not both 4, change to 5
    3. If current pixel is 6, left is 4, right is not 4: change to 5.

Vertical Rules:
    1. If a pixel is 0, and either top or bottom neighbor is 0 (but not both), change to 3.
    2. If a pixel is 0 and both top and bottom neighbors are NOT 0, change to 3.
    3. If a pixel is 0 and both top and bottom neighbors are 0, change to 3.
    4. If a pixel is yellow(4), and left and right neighbour are both green (3), it changes to Marron(9)
"""

import numpy as np

def get_horizontal_neighbors(grid, row, col):
    """Gets the immediate left and right neighbors of a pixel."""
    rows, cols = grid.shape
    left_neighbor = grid[row, col - 1] if col > 0 else None
    right_neighbor = grid[row, col + 1] if col < cols - 1 else None
    return left_neighbor, right_neighbor

def get_vertical_neighbors(grid, row, col):
    """Gets the immediate top and bottom neighbors of a pixel."""
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
            current_color = output_grid[row, col]
            left_neighbor, right_neighbor = get_horizontal_neighbors(input_grid, row, col)
            top_neighbor, bottom_neighbor = get_vertical_neighbors(input_grid, row, col)

            # Horizontal Rules
            if current_color == 4:
                if left_neighbor == 4 and right_neighbor == 4:
                    output_grid[row, col] = 6  # Rule 1
                elif not (left_neighbor == 4 and right_neighbor==4):
                    output_grid[row,col] = 5 # Rule 2
            elif current_color == 6:
                if left_neighbor == 4 and right_neighbor != 4:
                    output_grid[row, col] = 5  # Rule 3

            # Vertical Rules
            if current_color == 0:
                if (top_neighbor == 0 and bottom_neighbor != 0) or \
                   (top_neighbor != 0 and bottom_neighbor == 0):
                    output_grid[row, col] = 3  # Rule 1
                elif top_neighbor != 0 and bottom_neighbor != 0:
                    output_grid[row,col] = 3 #Rule 2.
                elif top_neighbor == 0 and bottom_neighbor == 0:
                    output_grid[row, col] = 3  # Rule 3
            elif current_color == 4: # Rule 4
                if left_neighbor == 3 and right_neighbor == 3:
                    output_grid[row,col] = 9



    return output_grid
```
```python
"""
Duplicates non-zero pixels in a grid if their right neighbor is the same color and their left neighbor is a different color or blank.
"""

import numpy as np

def get_neighbor(grid, row, col, direction):
    """Gets the neighbor of a cell in a given direction ('left' or 'right')."""
    height, width = grid.shape
    if direction == 'left':
        if col > 0:
            return grid[row, col - 1]
        else:
            return None  # No left neighbor
    elif direction == 'right':
        if col < width - 1:
            return grid[row, col + 1]
        else:
            return None  # No right neighbor
    return None

def transform(input_grid):
    """Transforms the input grid according to the duplication rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Start with a copy of the input
    height, width = input_grid.shape

    for row in range(height):
        for col in range(width):
            current_pixel = input_grid[row, col]

            # Skip if the current pixel is background (0)
            if current_pixel == 0:
                continue

            right_neighbor = get_neighbor(input_grid, row, col, 'right')
            left_neighbor = get_neighbor(input_grid, row, col, 'left')

            # Check conditions for duplication
            if right_neighbor is not None and right_neighbor == current_pixel:
                if left_neighbor is None or left_neighbor != current_pixel:
                    # Duplicate the pixel to the right of the right neighbor
                    if col + 2 < width: #make sure we can copy
                        output_grid[row, col + 2] = current_pixel

    return output_grid.tolist()
```

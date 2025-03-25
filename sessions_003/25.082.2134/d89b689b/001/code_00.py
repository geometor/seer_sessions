"""
The transformation rule involves identifying single pixels of specific colors and changing them to another color, while also removing any 2x2 blocks of azure (8). The color transformations are as follows:

- Orange (7) becomes Black (0)
- Magenta (6) becomes Blue (1)
- Yellow (4) becomes Green (3)
- Maroon (9) becomes Green (3)
- Gray (5) becomes Black (0)
- Blue (1) becomes Yellow (4)
- Red (2) becomes Magenta (6)
- Green (3) becomes Orange (7)
"""

import numpy as np

def is_single_pixel(grid, i, j):
    """Checks if a pixel is a single pixel (not part of a larger contiguous block)."""
    color = grid[i, j]
    if color == 0:
        return False

    height, width = grid.shape
    for x in range(max(0, i - 1), min(height, i + 2)):
        for y in range(max(0, j - 1), min(width, j + 2)):
            if (x, y) != (i, j) and grid[x, y] == color:
                return False
    return True

def remove_azure_blocks(grid):
    """Removes 2x2 azure blocks from the grid."""
    height, width = grid.shape
    output_grid = np.copy(grid)
    for i in range(height - 1):
        for j in range(width - 1):
            if (grid[i:i+2, j:j+2] == 8).all():
                output_grid[i:i+2, j:j+2] = 0
    return output_grid

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    # initialize output_grid
    output_grid = np.copy(input_grid)
    output_grid = remove_azure_blocks(output_grid)
    height, width = output_grid.shape
    # Create a copy to store changes, applying them after iterating
    changes = []

    # change output pixels based on color transformations
    for i in range(height):
        for j in range(width):
            if is_single_pixel(output_grid, i, j):
                current_color = output_grid[i, j]
                if current_color == 7:
                    changes.append(((i, j), 0))
                elif current_color == 6:
                    changes.append(((i, j), 1))
                elif current_color == 4:
                    changes.append(((i, j), 3))
                elif current_color == 9:
                    changes.append(((i, j), 3))
                elif current_color == 5:
                    changes.append(((i, j), 0))
                elif current_color == 1:
                    changes.append(((i, j), 4))
                elif current_color == 2:
                    changes.append(((i, j), 6))
                elif current_color == 3:
                    changes.append(((i, j), 7))
    for (i,j), new_color in changes:
      output_grid[i,j] = new_color
                    
    return output_grid
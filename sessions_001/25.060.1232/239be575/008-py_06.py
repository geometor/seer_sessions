"""
1.  **Count Red Pixels:** Count the number of red pixels in the input grid.
2.  **Count Azure Pixels:** Count the number of azure pixels in the input grid.
3. **Identify Red Rectangles:** Find ALL rectangular regions of red pixels.
4.  **Determine Output:**
      *  If there are any 4x1 (horizontal) or 1x4 (vertical) contiguous red pixels AND more azure than red, the output is 5.
      *  Otherwise, the output is 0.
"""

import numpy as np

def _find_red_rectangles(grid):
    """Finds all rectangular regions of red pixels."""
    rows, cols = grid.shape
    rectangles = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:  # Red pixel
                for height in range(1, rows - r + 1):
                    for width in range(1, cols - c + 1):
                        sub_grid = grid[r:r+height, c:c+width]
                        if np.all(sub_grid == 2):
                            rectangles.append((height, width))
    return rectangles

def transform(input_grid):
    # Count red pixels
    red_count = np.sum(input_grid == 2)

    # Count azure pixels
    azure_count = np.sum(input_grid == 8)

    # Find red rectangles
    red_rectangles = _find_red_rectangles(input_grid)

    # Determine output
    output_value = 0
    for height, width in red_rectangles:
        if (height == 1 and width == 4) or (height == 4 and width == 1):
            if azure_count > red_count:
                output_value = 5
                break

    # Create a 1x1 output grid
    output_grid = np.array([[output_value]])

    return output_grid
```python
"""
1.  **Scan the Input:** Traverse the input grid row by row, from top to bottom and left to right.
2.  **Identify Unique Colors:** For each row, maintain a list of colors, only adding colors that haven't yet been added.
3.  **Arrange in Output:** Arrange the unique colors in a 3x4 grid. Starting from top left, insert colors, moving to the right and then the next row.
4.  **Output:** Return 3 x 4 grid
"""

import numpy as np

def get_unique_colors(input_grid):
    """Extract unique colors from the input grid in row-major order."""
    unique_colors = []
    for row in input_grid:
        for pixel in row:
            if pixel != 0 and pixel not in unique_colors:
                unique_colors.append(pixel)
    return unique_colors

def transform(input_grid):
    """Transforms the input grid into a 3x4 grid of unique colors."""

    # Extract unique colors
    unique_colors = get_unique_colors(input_grid)

    # Initialize output grid
    output_grid = np.zeros((3, 4), dtype=int)

    # Fill the output grid
    color_index = 0
    for i in range(3):
        for j in range(4):
            if color_index < len(unique_colors):
                output_grid[i, j] = unique_colors[color_index]
                color_index += 1

    return output_grid
```
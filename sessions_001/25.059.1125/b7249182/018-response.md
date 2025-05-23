# b7249182 • 018 • refine_coder

---
```python
"""
1.  **Identify Non-Zero Pixels:** Find all pixels in the input grid that have a value other than 0. These pixels act as the centers of crosses.
2.  **Create Crosses:** For each non-zero pixel:
    *   Create a cross shape centered at the pixel's original location (row, column).
    *   The cross is formed from pixels of the *same color* as the original pixel.
    * The cross consists of a horizontal line and a vertical line.
    *   Each arm of the cross extends *one* pixel away from the center. Meaning the total width and height of the cross is 3 pixels.
3.  **Output:** The output grid is initialized as all zeros. Crosses are drawn onto this grid. If crosses overlap, the pixel value of the most recently drawn cross is used.
"""

import numpy as np

def find_non_zero_pixels(grid):
    """Finds the coordinates and values of non-zero pixels in a grid."""
    non_zero_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value != 0:
                non_zero_pixels.append(((row_index, col_index), value))
    return non_zero_pixels

def create_cross(grid, center, value):
    """Creates a cross shape in the grid centered at the given coordinates."""
    row, col = center
    height, width = grid.shape

    # Horizontal part of the cross (3 pixels wide)
    for i in range(max(0, col - 1), min(width, col + 2)):
        grid[row, i] = value

    # Vertical part of the cross (3 pixels high)
    for i in range(max(0, row - 1), min(height, row + 2)):
        grid[i, col] = value


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid as all zeros
    output_grid = np.zeros_like(input_grid)

    # Find non-zero pixels
    non_zero_pixels = find_non_zero_pixels(input_grid)

    # Create crosses for each non-zero pixel
    for (row, col), value in non_zero_pixels:
        create_cross(output_grid, (row, col), value)

    return output_grid
```


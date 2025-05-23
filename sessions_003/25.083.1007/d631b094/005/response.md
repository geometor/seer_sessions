```python
"""
1.  **Identify Target Color:** Find the single non-zero color (the "target color") within the input grid. If no non-zero color exists, return an empty grid.

2.  **Count Target Color Occurrences:**
    *   `top_count`: Count how many times the target color appears in the first row of the input grid.
    *   `side_count`: Count how many times the target color appears in the first column of the input grid.

3.  **Determine Output Grid Dimensions:**
    *   The output grid's height will always be 1.
    *   The output grid's width is calculated as `top_count + side_count + 1` if both are greater or equal to zero.
      If only side_count is zero, then `width = top_count`.
     If only `top_count` is zero, then `width = side_count * (top_count+1)`

4.  **Create and Populate Output Grid:** Create a new grid with the calculated dimensions (1 x width). Fill every cell of this grid with the target color.

5.  **Return Output Grid:** Return the created grid.
"""

import numpy as np

def get_target_color(grid):
    # Find the unique non-zero color in the grid
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return 0

def count_top_side(grid, target_color):
    # Count target color occurrences in the first row (top_count)
    top_count = np.sum(grid[0] == target_color)
    # Count target color occurrences in the first column (side_count)
    side_count = np.sum(grid[:, 0] == target_color)
    return top_count, side_count

def transform(input_grid):
    # Find the target (non-zero) color
    target_color = get_target_color(input_grid)

    # If no target color, return an empty grid
    if target_color == 0:
        return np.array([])

    # Count target color occurrences
    top_count, side_count = count_top_side(input_grid, target_color)

    # Determine output grid dimensions
    height = 1
    if top_count == 0:
        width = side_count
    elif side_count == 0:
        width = top_count
    else:
        width = top_count + side_count + 1

    # Create and populate the output grid
    output_grid = np.full((height, width), target_color)

    return output_grid
```
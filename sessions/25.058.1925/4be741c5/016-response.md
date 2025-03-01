# 4be741c5 • 016 • example_3 • investigate_coder

---
```python
"""
Scans the input grid vertically, extracts unique colors in order of their first appearance,
and creates a 1D output grid representing those colors.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 2D grid into a 1D grid containing the unique colors
    encountered in a top-down, column-by-column scan.

    Args:
        input_grid (list of lists): The input 2D grid.

    Returns:
        list: A 1D grid (list) of unique colors.
    """
    unique_colors = []
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Scan the input grid column by column, top to bottom.
    for col in range(cols):
        for row in range(rows):
            color = input_grid[row][col]
            # If the color is not already in the list, add it.
            if color not in unique_colors:
                unique_colors.append(color)

    # Convert to numpy array
    output_grid = np.array(unique_colors).reshape(-1, 1)

    return output_grid.tolist()
```

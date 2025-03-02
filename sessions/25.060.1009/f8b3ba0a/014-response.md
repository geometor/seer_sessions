# f8b3ba0a • 014 • refine_coder

---
```python
"""
1. **Identify Unique Colors:** Examine the input grid and identify all unique colors present, excluding the background color (0).
2. **Order Colors (Reading Order):** Order the identified colors based on their first appearance in the input grid. The order follows a top-to-bottom, then left-to-right traversal of the grid (similar to reading order).
3. **Create Output Grid:** Construct a new grid with dimensions Nx1, where N is the number of unique colors found. Each cell in the output grid contains one of the ordered colors, maintaining the established sequence.
"""

import numpy as np

def get_colors_in_reading_order(grid):
    """
    Returns a list of unique colors in the grid, ordered as if reading
    the grid from top to bottom, then left to right.
    """
    rows, cols = grid.shape
    colors_found = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color not in colors_found:
                colors_found.append(color)
    return colors_found

def transform(input_grid):
    """Transforms the input grid to output a vertical grid of unique colors in reading order."""
    # Get unique colors in reading order
    ordered_colors = get_colors_in_reading_order(input_grid)

    # Create output grid
    output_grid = np.array(ordered_colors).reshape(-1, 1)

    return output_grid
```

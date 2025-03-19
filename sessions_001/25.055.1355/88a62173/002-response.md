# 88a62173 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Focus:** Examine the top-left 2x2 region of the input grid.
2.  **Quadrant Summary**: Consider a 2x2 sub-grid
3.  **Populate Output**: Create an output grid of size 2x2. Populate the first three elements (reading order) from the 2x2 sub-grid. For the last position, place the color of that subgrid that occupies most positions.
"""

import numpy as np

def get_top_left_2x2(grid):
    """Extracts the top-left 2x2 subgrid."""
    return grid[:2, :2]

def most_common_color(grid):
    """Finds the most common color in a grid."""
    unique, counts = np.unique(grid, return_counts=True)
    return unique[np.argmax(counts)]

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Focus on the top-left 2x2 region.
    top_left_2x2 = get_top_left_2x2(input_grid)

    # 2. Create an output grid of size 2x2.
    output_grid = np.zeros((2, 2), dtype=int)

    # 3. Populate Output
    output_grid[0, 0] = top_left_2x2[0, 0]
    output_grid[0, 1] = top_left_2x2[0, 1]
    output_grid[1, 0] = top_left_2x2[1, 0]
    output_grid[1, 1] = most_common_color(top_left_2x2)

    return output_grid.tolist()
```

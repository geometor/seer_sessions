# d8c310e9 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule takes the pattern found on the last two rows and replicates it horizontally across the entire width of the last two rows.
"""

import numpy as np

def get_pattern(grid):
    # Extract the last two rows
    pattern = grid[-2:, :]
    return pattern

def extend_pattern(grid, pattern):
    # Get dimensions of the grid and pattern
    grid_height, grid_width = grid.shape
    pattern_height, pattern_width = pattern.shape

    # Initialize the output grid with the same dimensions as the input
    output_grid = np.zeros_like(grid)
    # Fill the output grid with white
    output_grid[:] = 0

    # Fill in last two rows
    for col_start in range(0, grid_width, pattern_width):
        # Ensure we don't go out of bounds
        col_end = min(col_start + pattern_width, grid_width)
        actual_pattern_width = col_end - col_start
        output_grid[-2:, col_start:col_end] = pattern[:, :actual_pattern_width]

    return output_grid

def transform(input_grid):
    """
    Extends a pattern from the last two rows across the entire width.
    """
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)

    # Extract repeating pattern
    pattern = get_pattern(input_grid)

    # build grid from pattern
    output_grid = extend_pattern(input_grid, pattern)


    return output_grid.tolist()
```

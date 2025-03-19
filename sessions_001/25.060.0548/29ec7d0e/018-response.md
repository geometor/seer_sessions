# 29ec7d0e • 018 • refine_coder

---
```python
"""
The transformation rule is as follows:
1. Identify the Repeating Pattern: Extract the 7x7 grid from the top-left corner of the input grid. This is the `repeating_pattern`.
2. Overlay the Pattern: Copy the `repeating_pattern` onto the output grid. Start at the top-left corner (0,0) of the output grid.
3. Repeat Overlay: Repeat the overlay process, shifting the starting position of the `repeating_pattern` by 7 units horizontally and vertically. Continue this repetition until the entire output grid is covered. All pixels in positions corresponding to the repeating pattern should take the value in the repeating pattern.
"""

import numpy as np

def get_repeating_pattern(grid, pattern_size=7):
    """Extracts the repeating pattern from the grid."""
    pattern = grid[:pattern_size, :pattern_size]
    return pattern

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = input_grid.copy()
    pattern_size = 7
    pattern = get_repeating_pattern(input_grid, pattern_size)

    rows, cols = input_grid.shape

    # Iterate through the entire grid, applying the pattern
    for r in range(rows):
        for c in range(cols):
            # Overlay the pattern, repeating it every pattern_size
            output_grid[r, c] = pattern[r % pattern_size, c % pattern_size]

    return output_grid.tolist()
```


# 0a938d79 • 014 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  Identify Unique Colors: Find all unique, non-zero colors present in the input grid.
2.  Create Base Pattern: Construct a base pattern by taking each unique color and appending two zeros after it. The colors are sorted in ascending order.
3. Apply Pattern: Construct the output by repeating this pattern across all rows.
"""

import numpy as np

def find_unique_colors(grid):
    """Finds all unique non-zero colors in a grid."""
    return sorted(list(np.unique(grid[grid != 0])))

def create_base_pattern(unique_colors):
    """Creates the base pattern: [color1, 0, 0, color2, 0, 0, ...]."""
    pattern = []
    for color in unique_colors:
        pattern.extend([color, 0, 0])
    return pattern

def transform(input_grid):
    """Transforms the input grid based on the defined rule."""
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find unique colors
    unique_colors = find_unique_colors(input_grid)

    # Create base pattern
    base_pattern = create_base_pattern(unique_colors)

    # Apply pattern to each row
    for i in range(output_grid.shape[0]):
        output_grid[i] = np.tile(base_pattern, output_grid.shape[1] // len(base_pattern) + 1)[:output_grid.shape[1]]

    return output_grid
```

```python
"""
1.  **Identify the most frequent color:** Determine the most frequent color across the *entire* input grid.
2.  **Replace other colors:** In the output grid, replace all pixels that *do not* match the most frequent color (identified in step 1) with the color gray (5).
3.  Pixels matching the most frequent color retain their original color.
"""

import numpy as np
from collections import Counter

def get_most_frequent_color(grid):
    """Helper function to find the most frequent color in the entire grid."""
    color_counts = Counter(grid.flatten())
    return color_counts.most_common(1)[0][0]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify the most frequent color in the entire grid
    most_frequent_color = get_most_frequent_color(input_grid)

    # Iterate through the entire grid
    for r in range(rows):
        for c in range(cols):
            # Replace non-most-frequent colors with 5 (gray)
            if output_grid[r, c] != most_frequent_color:
                output_grid[r, c] = 5

    return output_grid
```

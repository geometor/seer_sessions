# d2abd087 • 018 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1. Identify Gray Regions: Find all pixels in the input grid that are gray (value 5).
2. Classify Regions: Divide the gray pixels into two distinct groups. The grouping criteria is based on x-coordinate. Pixels with x-coordinate less than 7 belong to group 1; the rest belong to the group 2.
3. Recolor:
    *   Change the color of the gray pixels in the first group to blue (value 1).
    *   Change the color of the gray pixels in the second group to red (value 2).
4. Preserve White: Keep all white pixels (value 0) unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is gray
            if output_grid[r, c] == 5:
                # Classify and recolor based on x-coordinate
                if c < 7:
                    output_grid[r, c] = 1  # Blue
                else:
                    output_grid[r, c] = 2  # Red

    return output_grid
```

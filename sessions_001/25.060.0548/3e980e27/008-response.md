# 3e980e27 • 008 • refine_coder

---
```python
"""
Copies the input grid to the output grid. Then, finds vertically stacked pairs of red pixels and adds a blue pixel directly below the bottom red pixel of the pair.
"""

import numpy as np

def find_vertical_red_pairs(grid):
    """Finds pairs of vertically stacked red pixels."""
    red_pixels = np.argwhere(grid == 2)
    pairs = []
    for i in range(len(red_pixels)):
        for j in range(i + 1, len(red_pixels)):
            if red_pixels[i][1] == red_pixels[j][1] and red_pixels[j][0] == red_pixels[i][0] + 1:
                pairs.append((red_pixels[i], red_pixels[j]))
    return pairs

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find vertically stacked pairs of red pixels
    red_pairs = find_vertical_red_pairs(input_grid)

    # Add a blue pixel below the bottom red pixel of each pair
    for pair in red_pairs:
        bottom_red_y, bottom_red_x = pair[1]
        if bottom_red_y + 1 < output_grid.shape[0]:
            output_grid[bottom_red_y + 1, bottom_red_x] = 1

    return output_grid
```

# f8c80d96 • 004 • example_1 • investigate_coder

---
```python
"""
The azure (8) pixels in the input grid act as "seed" points for an azure and gray checkerboard pattern that propagates across the entire output grid, anchored at the top-left pixel in relation to the first azure seed pixel encountered.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with the same dimensions as the input.
    output_grid = np.full(input_grid.shape, -1)  # -1 represents unvisited

    # Find seed points (azure pixels in input)
    seed_points = np.argwhere(input_grid == 8)

    # Fill first seed point and mark as visited
    if len(seed_points)>0:
        first_seed = tuple(seed_points[0])
        output_grid[first_seed] = 8

    # Checkerboard fill.
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if input_grid[r,c]==8:
                output_grid[r,c] = 8
            else:
                if (r + c) % 2 == (first_seed[0]+first_seed[1])%2: # use first_seed point
                    output_grid[r,c] = 8
                else:
                    output_grid[r, c] = 5

    return output_grid
```

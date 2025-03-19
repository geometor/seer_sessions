# 88a62173 • 004 • refine_coder

---
```python
"""
1.  **Iterate:** Consider all possible, overlapping 2x2 subgrids within the input grid.
2.  **Most Common Color:** For each 2x2 subgrid, find the most frequent color. If there are multiple colors with the same highest frequency, select the top-left pixel's color in that 2x2 subgrid.
3.  **Populate:** The 2x2 output uses the top-left value from each overlapping 2x2 square in the input.
"""

import numpy as np

def get_all_2x2_subgrids(grid):
    """Extracts all possible 2x2 subgrids from the input grid."""
    subgrids = []
    for i in range(grid.shape[0] - 1):
        for j in range(grid.shape[1] - 1):
            subgrids.append(grid[i:i+2, j:j+2])
    return subgrids

def most_common_color_with_top_left_tiebreaker(subgrid):
    """Finds the most frequent color.  If tie, use top-left."""
    unique, counts = np.unique(subgrid, return_counts=True)
    if len(counts) > 1 and counts[0] == counts[1]:
       return subgrid[0,0]
    return unique[np.argmax(counts)]

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # Initialize output grid (always 2x2)
    output_grid = np.zeros((2, 2), dtype=int)

    # Get all 2x2 subgrids
    #subgrids = get_all_2x2_subgrids(input_grid)

    # Populate the output grid.
    output_grid[0, 0] = input_grid[0, 0]
    output_grid[0, 1] = input_grid[0, 1]
    output_grid[1, 0] = input_grid[1, 0]
    output_grid[1, 1] = most_common_color_with_top_left_tiebreaker(input_grid[0:2, 0:2])

    return output_grid.tolist()
```

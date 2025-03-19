# 88a62173 • 006 • refine_coder

---
```python
"""
1.  **Copy:** The top-left, top-right and bottom-left pixels from the 2x2 subgrid at the top-left of the input grid and place in the output grid.
2.  **Subgrid:** Create a 2x2 subgrid using the top-left corner of the input.
3.  **Most Frequent Color:** Examine the 2x2 subgrid, determine the most frequent color. If there is a tie for the most frequent color, select the color of the top-left pixel of the subgrid.
4. **Bottom-Right:** Place the most frequent color (or tie-breaker) in the bottom-right pixel of the output grid.
"""

import numpy as np

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

    # Copy top-left, top-right, and bottom-left pixels
    output_grid[0, 0] = input_grid[0, 0]
    output_grid[0, 1] = input_grid[0, 1]
    output_grid[1, 0] = input_grid[1, 0]

    # Determine bottom-right pixel using the 2x2 subgrid and most frequent color
    output_grid[1, 1] = most_common_color_with_top_left_tiebreaker(input_grid[0:2, 0:2])

    return output_grid.tolist()
```


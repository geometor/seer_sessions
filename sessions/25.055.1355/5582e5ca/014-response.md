# 5582e5ca • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to identify the most frequent color in the input grid and create an output grid of the same dimensions, filled entirely with that color.
"""

import numpy as np

def get_most_frequent_color(grid):
    # Flatten the grid to a 1D array
    flat_grid = grid.flatten()
    # Count the occurrences of each color
    unique, counts = np.unique(flat_grid, return_counts=True)
    # Get color with max count
    most_frequent_color = unique[np.argmax(counts)]
    return most_frequent_color

def transform(input_grid):
    # initialize output_grid with same dimensions
    output_grid = np.zeros_like(input_grid)

    # Find the most frequent color in the input grid
    most_frequent_color = get_most_frequent_color(input_grid)

    # Fill the output grid with the most frequent color
    output_grid[:] = most_frequent_color

    return output_grid
```

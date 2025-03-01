# 6f8cd79b • 006 • refine_coder

---
```python
"""
Identify all 3x3 subgrids within the input grid. For each subgrid, check if all its pixels
have the same color and the color is not black (0). If they do, keep the center pixel's
color unchanged and change the color of all surrounding pixels to 8 (azure).
"""

import numpy as np

def is_homogeneous(subgrid):
    """Checks if all elements in a subgrid are the same and not 0."""
    first_element = subgrid.flatten()[0]
    if first_element == 0:
        return False
    return np.all(subgrid == first_element)

def transform(input_grid):
    """
    Transforms the input grid by applying the rule to all 3x3 subgrids that are homogeneous and non-black.
    """
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Initialize output as a copy

    # Iterate through all possible top-left corners of 3x3 subgrids
    for i in range(rows - 2):
        for j in range(cols - 2):
            # Extract the current 3x3 subgrid
            subgrid = input_grid[i:i+3, j:j+3]

            # Check for homogeneity and non-black color
            if is_homogeneous(subgrid):
                # Apply the transformation to the current 3x3 subgrid
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        if x == i + 1 and y == j + 1:  # Center pixel
                            continue  # Keep center pixel unchanged
                        else:
                            output_grid[x, y] = 8  # Set surrounding pixels to azure

    return output_grid
```

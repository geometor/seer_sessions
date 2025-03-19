# 2dee498d • 007 • refine_coder

---
```python
"""
Extracts unique colors from the input grid, preserving the order of their first appearance, and arranges them in a single-row output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting unique colors in order of appearance.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with unique colors in a single row.
    """
    # Initialize an empty list to store unique colors
    unique_colors = []

    # Iterate through the input grid row by row, then column by column
    for row in input_grid:
        for cell in row:
            # If the color hasn't been seen before, add it to the list
            if cell not in unique_colors:
                unique_colors.append(cell)

    # Create the output grid as a single row
    output_grid = [unique_colors]

    return output_grid
```


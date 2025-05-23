# 1fad071e • 004 • example_1 • investigate_coder

---
```python
"""
The transformation extracts a sequence of color values from the input grid and uses them to populate a smaller output grid. Specifically, it appears to:

1. Examine the first and last rows of the input grid.
2.  Record the unique colors encountered, in order of their first appearance, prioritizing left-to-right order.
3. Create a 1x5 output grid.
4. Populate the output grid with the recorded sequence of colors.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 9x9 input grid into a 1x5 output grid by extracting a sequence of colors from the first and last rows."""

    # Initialize the output grid as a 1x5 array filled with zeros (white).
    output_grid = np.zeros((1, 5), dtype=int)

    # Extract the first and last rows of the input grid.
    first_row = input_grid[0, :]
    last_row = input_grid[-1, :]

    # Combine both rows into a single sequence for easier processing.
    combined_rows = np.concatenate((first_row, last_row))

    # Find unique colors in order of appearance.
    unique_colors = []
    for color in combined_rows:
        if color not in unique_colors:
            unique_colors.append(color)

    # Populate the output grid with the unique colors, up to its capacity.
    for i in range(min(len(unique_colors), 5)):
        output_grid[0, i] = unique_colors[i]
        

    return output_grid
```

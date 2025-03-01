# 1e0a9b12 • 002 • example_1 • investigate_coder

---
```python
"""
1. Identify all non-zero elements in the input grid.
2. Collect these non-zero values.
3. Place these collected values, in order of their original appearance in the input (reading left-to-right, top-to-bottom), into the last row of the output grid, starting from the bottom-leftmost cell.
4. Fill all other cells in the output grid with zeros (white).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Collect non-zero elements
    non_zero_elements = []
    for row in input_grid:
        for element in row:
            if element != 0:
                non_zero_elements.append(element)

    # Place collected elements in the last row of the output grid
    last_row_index = output_grid.shape[0] - 1
    for i, element in enumerate(non_zero_elements):
        output_grid[last_row_index, i] = element

    return output_grid
```


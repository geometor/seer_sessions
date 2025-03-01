# 90c28cc7 • 008 • refine_coder

---
```python
"""
The transformation extracts the first non-zero color from each row of the input grid,
and creates a single-row output grid containing these colors in order, excluding rows
where the first non-zero element is 0 (all-zero rows).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into a single-row output grid by extracting
    the first non-zero color from each row, excluding all-zero rows.
    """
    # Initialize an empty list to store the first non-zero colors
    first_non_zero_colors = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Find all non-zero elements in the current row
        non_zero_elements = row[row != 0]

        # If there are non-zero elements, append the first one to the list
        if non_zero_elements.size > 0:
            first_non_zero_colors.append(non_zero_elements[0])

    # Create the output grid as a single row with the collected colors
    output_grid = np.array(first_non_zero_colors).reshape(1, -1)

    return output_grid
```

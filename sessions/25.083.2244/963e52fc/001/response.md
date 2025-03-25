```python
"""
Iterates through each row of the input grid. If a row contains only zeros, it remains unchanged in the output grid.
Otherwise, the row's width is doubled by duplicating its sequence of pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as an empty list to hold rows
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Check if the row contains only zeros
        if np.all(np.array(row) == 0):
            # If all zeros, append the original row to the output_grid
            output_grid.append(list(row) + [0] * len(row)) # pad with zeros to correct dimensions
        else:
            # If not all zeros, double the width of the row
            expanded_row = list(row) + list(row)
            # Append the expanded row to the output_grid
            output_grid.append(expanded_row)

    return output_grid
```
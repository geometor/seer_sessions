# e98196ab • 014 • refine_coder

---
```python
"""
Examine each row of the input grid. If a row contains only grey (5) pixels or only black (0) pixels, remove it. Keep all other rows, maintaining their original order and pixel positions. The output grid consists of the remaining rows.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a list of rows
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Check if the row contains only grey (5) or only black (0) pixels
        unique_colors = np.unique(row)
        if (len(unique_colors) == 1 and (unique_colors[0] == 5 or unique_colors[0] == 0)) or (len(unique_colors) == 2 and 0 in unique_colors and 5 in unique_colors)  :
            # If it contains only grey or black, skip this row (don't add it to the output)
            continue
        else:
            # Otherwise, keep the row by appending it to output_grid
            output_grid.append(row)

    # convert the list of rows to a numpy array
    return np.array(output_grid)
```


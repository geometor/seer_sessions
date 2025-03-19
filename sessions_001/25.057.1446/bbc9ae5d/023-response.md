# bbc9ae5d • 023 • refine_coder

---
```python
"""
1.  Examine each row of the input grid.
2.  Check for the presence of a maroon (value 9) pixel in the current row.
3.  If a maroon pixel is found, keep that row in the output grid.
4. If no rows have a maroon pixel, then the output is identical to the input
5.  If no maroon pixel is found in *any* row, return the entire input grid.
6.  The result is a new grid containing only the rows with maroon pixels (or the original grid if no maroon pixels are present).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of maroon (9) pixels.
    """
    input_grid = np.array(input_grid)
    output_rows = []
    maroon_present = False

    # Iterate through each row of the input grid
    for row in input_grid:
        # Check if the maroon pixel (9) is present in the current row
        if 9 in row:
            maroon_present = True
            output_rows.append(row)

    # If no maroon pixels were found, return the original grid
    if not maroon_present:
        return input_grid
    # Otherwise, construct the output grid from the selected rows
    else:
        return np.array(output_rows)
```


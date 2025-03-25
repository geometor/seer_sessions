```python
"""
Iterate through each row of the input grid. If a row contains any blue (1) pixels, replace all blue pixels in that row with red (2) pixels, and duplicate the modified row, appending both to a list of output rows. Finally, return these rows as the new grid.
"""

import numpy as np

def transform(input_grid):
    output_rows = []
    input_grid = np.array(input_grid)

    # Iterate through each row.
    for row in input_grid:
        # Check if the row contains any blue pixels.
        if 1 in row:
            # Replace blue pixels with red pixels.
            new_row = [2 if cell == 1 else cell for cell in row]
            # Duplicate and add the new rows
            output_rows.append(new_row)
            output_rows.append(new_row)

    return output_rows
```
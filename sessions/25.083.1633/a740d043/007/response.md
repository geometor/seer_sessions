```python
"""
Transforms the input grid by extracting the sequence of non-background colors
from each row, discarding spatial information, and constructing an output grid
whose height equals the number of rows with colors and width is equal to the
longest sequence of non-background colors.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rules described above.
    """
    input_grid = np.array(input_grid)
    output_rows = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Extract non-background (non-1) colors, preserving order
        non_background_colors = [pixel for pixel in row if pixel != 1]

        # If the row contains non-background colors, add to output_rows
        if non_background_colors:
            output_rows.append(non_background_colors)

    # Determine output grid height (number of non-empty rows)
    output_height = len(output_rows)
    
    # if no rows have colors return empty array
    if output_height == 0:
        return []

    # Determine output grid width (maximum length of non-background color sequences)
    output_width = max(len(row) for row in output_rows)

    # Build the output grid, padding shorter rows with 0s if necessary.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    for i, row in enumerate(output_rows):
      for j, pixel in enumerate(row):
        output_grid[i,j] = pixel

    return output_grid.tolist()
```
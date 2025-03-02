"""
1.  **First Row Transformation:** The first row (index 0) of the input grid is always transformed to gray (color code 5) in the output grid.
2.  **Other Rows Transformation:** For all rows below the first row (index > 0), identify the primary (most frequent) color in the rows of the input that are *not* the first row. The primary color for these rows will be the output color of the entire row. Transform the entire row to this identified primary color.
3. **Shape Preservation**: The height and width of the grid remain unchanged.
"""

import numpy as np
from collections import Counter

def _get_primary_color_excluding_first_row(grid):
    # Flatten the grid excluding the first row
    flattened_grid = grid[1:, :].flatten()
    # Count color occurrences
    color_counts = Counter(flattened_grid)
    # Return the most common color (primary color)
    most_common_color = color_counts.most_common(1)
    if most_common_color:
      return most_common_color[0][0]
    else:
      return 0 # default to white in case no other rows exist or there is not primary color.

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input.
    output_grid = np.copy(input_grid)

    # Transform the first row to gray (5).
    output_grid[0, :] = 5

    # Transform other rows based on the primary color excluding the first row.
    primary_color = _get_primary_color_excluding_first_row(input_grid)
    output_grid[1:, :] = primary_color

    return output_grid
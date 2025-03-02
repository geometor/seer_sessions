"""
1.  **Identify Unique Colors Per Column:** Examine each column of the input grid independently. For each column identify the unique color, ignoring duplicates if a column only containts one color it becomes the unique color.
2.  **Construct Output Row:** Create a new row. For each column in the original grid, place the identified (or deduplicated) color in the output row, the output row should now have as many items as there are unique colors per column in the input..
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid to the output grid."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = []

    # Iterate through columns
    for j in range(cols):
        unique_colors = []
        # Iterate through rows in the current column
        for i in range(rows):
            color = input_grid[i, j]
            if color not in unique_colors:
                unique_colors.append(color)
        #if a column only had one number to begin with, there is nothing to remove
        if len(unique_colors) == 1:
          output_grid.append(unique_colors[0])

    return output_grid
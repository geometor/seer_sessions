"""
1.  **Grid Expansion:** Double the input grid's dimensions (height and width).

2.  **Magenta Replication:** For each magenta pixel in the *original* input grid, place a magenta pixel at the same row and column in the output grid.  Additionally, place another magenta pixel in the same row, but with its column position increased by *half the width of the original input grid*.

3.  **Azure Filling:**
    *   Iterate through the *rows* of the *output grid*. If a row contains at least one magenta pixel, fill all blank (white, 0) pixels in that row with azure (8).
    *   Identify all rows in the *input grid* that have one or more magenta pixels.
    *   In the expanded grid, fill all the cells in rows between the lowest and highest of these rows with azure.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # magenta replication
    for row in range(input_height):
        for col in range(input_width):
            if input_grid[row, col] == 6:
                output_grid[row, col] = 6
                output_grid[row, col + (input_width // 2)] = 6

    # azure fill rows with magenta
    for row in range(output_height):
        if 6 in output_grid[row]:
            output_grid[row,:] = [8 if x == 0 else x for x in output_grid[row,:] ]

    # azure fill between rows
    magenta_rows = [ r for r in range(input_height) if 6 in input_grid[r,:] ]
    if len(magenta_rows) > 0 :
        min_magenta_row = min(magenta_rows)
        max_magenta_row = max(magenta_rows)
        for row in range(min_magenta_row, max_magenta_row + 1):
          for col in range(output_width):
            if output_grid[row, col] == 0:
                output_grid[row,col] = 8
    
    return output_grid
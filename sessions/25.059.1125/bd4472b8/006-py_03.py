"""
1.  **Input:** A 2D grid of colors.
2.  **Determine Output Dimensions:** The output grid has the same number of columns as the input grid. The output grid's height is twice the input grid's height.
3.  **Replicate First Row:** Copy the colors from the first row of the input grid into the output grid. Repeat this copy a second time immediately below.
4.  **Replicate Second Row:** Copy the colors from the second row of the input grid into the output grid, directly below the last replicated first row. Repeat this copy a second time immediately below.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the described rule.
    """
    # Determine output dimensions.
    output_height = 2 * input_grid.shape[0]
    output_width = input_grid.shape[1]
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Replicate first row.
    first_row = input_grid[0]
    output_grid[0] = first_row
    output_grid[1] = first_row

    # Replicate second row.
    second_row = input_grid[1]
    output_grid[2] = second_row
    output_grid[3] = second_row
    
    # Generalize the replication for any input height.
    for i in range(2, input_grid.shape[0]):
        output_grid[i*2] = input_grid[i]
        output_grid[i*2 + 1] = input_grid[i]

    return output_grid
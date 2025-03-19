"""
1.  **Identify the Central Stripe:** Locate the vertical stripe of blue (color 1) pixels in the input grid. This stripe acts as the primary source of transformation.
2. **Extract column:** Use central column to create new grid
3.  **Resize:** Create a new grid with the same height as the input stripe but a new width, which would be fixed number.
4.  **Color Mapping:**
    *   Change all blue pixels from the original stripe to azure (color 8).
    *   Change all the other pixels to the white (color 0).
5. **Create checkered pattern:** Create 3-wide vertical pattern where color alternates white-azure-azure in a column, but in the next row it is offset and starts azure-white-azure.
"""

import numpy as np

def get_central_stripe(grid):
    # Find the column index with the most blue pixels
    num_rows, num_cols = grid.shape
    blue_counts = []
    for j in range(num_cols):
      blue_counts.append(np.sum(grid[:,j]==1))

    # find column of max blue pixels
    center_col = blue_counts.index(max(blue_counts))

    # return that column
    return grid[:, center_col]

def transform(input_grid):
    # Find the central blue stripe.
    central_stripe = get_central_stripe(input_grid)

    # Initialize the output grid.
    num_rows = len(central_stripe)
    num_cols_out = 3
    output_grid = np.zeros((num_rows, num_cols_out), dtype=int)


    # Populate the output grid.
    for i in range(num_rows):
        if central_stripe[i] == 1:
          if i % 2 == 0:
            output_grid[i,:] = [0,8,8]
          else:
            output_grid[i,:] = [8,0,8]
        else:
            if i % 2 == 0:
              output_grid[i,:] = [0,0,0]
            else:
              output_grid[i,:] = [0,0,0]          

    return output_grid
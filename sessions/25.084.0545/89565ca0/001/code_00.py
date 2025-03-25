"""
The input grid is summarized by identifying the colors that form large blocks that span the full width.
For each such color, create a row in output grid with that color repeated four times.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into a summarized output grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    output_grid = []
    rows_processed = []

    # Iterate through each row of the input grid
    for i, row in enumerate(input_grid):
      # Check if the row has already been processed
        if i in rows_processed:
            continue

        unique_colors = np.unique(row)
        width = len(row)
      
        for color in unique_colors:
            color_indices = np.where(row == color)[0]

            # Identify full-width blocks
            if len(color_indices) > 0:
              # Check if there are runs of this color that span the entire width of the grid.
              is_full_width = False
              
              if (np.max(color_indices) - np.min(color_indices) + 1) == width :
                is_full_width = True

              if is_full_width:
                 # Construct the output row (color repeated four times)
                  output_row = [color] * 4
                  output_grid.append(output_row)

                  # Find other rows that are exactly the same for this color
                  for j in range(i + 1, len(input_grid)):
                    next_row = input_grid[j]
                    next_color_indices = np.where(next_row == color)[0]
                    next_is_full_width = False
                    if len(next_color_indices) > 0:
                        if (np.max(next_color_indices) - np.min(next_color_indices) + 1) == width :
                          next_is_full_width = True

                    if next_is_full_width and np.array_equal(input_grid[i], input_grid[j]):
                      rows_processed.append(j) # Mark as processed to skip next time
                  break  # only need one line to represent all that are the same


    return np.array(output_grid)
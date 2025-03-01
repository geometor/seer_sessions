"""
The transformation rule is to remove all occurrences of the digit '0' (representing white pixels) from the input grid to produce the output grid. The relative order and arrangement of the non-zero digits are preserved. Essentially, the rule "erases" or "filters out" the white background, leaving only the colored patterns intact and making them fill the complete grid without any gaps.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing all '0' pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid with '0' pixels removed.
    """
    # Convert the input grid to a numpy array if it isn't already.
    input_grid = np.array(input_grid)

    # Create a new grid by filtering out all '0' elements.
    # Flatten, filter, and then reshape.
    filtered_pixels = input_grid[input_grid != 0]
    
    rows, cols = input_grid.shape
    
    new_rows = rows
    new_cols = cols
    
    output_grid = np.full((new_rows, new_cols), 1, dtype=int)
    
     # Calculate index for placing next non-zero.
    next_index = 0  

    # Iterate through cells and insert non-zero pixels.
    for r in range(rows):
        for c in range(cols):
          if (input_grid[r, c] != 0):
              output_r = next_index // new_cols
              output_c = next_index % new_cols

              output_grid[output_r, output_c] = input_grid[r,c]
              next_index += 1

    return output_grid
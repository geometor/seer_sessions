"""
1.  **Scan the input grid:** Traverse the input grid, observing the color of each pixel.
2.  **Identify non-gray pixels before gray pixels:** consider the pixels going from left to right and top to bottom, keep track of the sequence of non-gray pixels that preceed a gray pixel.
3.  **Extract and Order:** Extract these "pre-gray" non-gray pixels and place them sequentially into a new 1-dimensional array.
4.  **Output:** The output grid is this new 1-dimensional array.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid by extracting non-gray pixels that appear immediately before gray pixels."""

    output_list = []
    rows, cols = input_grid.shape
    
    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Check for gray pixel
            if input_grid[r, c] == 5:
                # Check if there's a preceding non-gray pixel in the same row
                if c > 0 and input_grid[r, c-1] != 5:
                    output_list.append(input_grid[r, c-1])

    # Convert the list to a NumPy array (output grid)
    output_grid = np.array(output_list)
    if len(output_grid)>0:
        output_grid = output_grid.reshape(1, -1)  # Reshape to 1 row
    else:
         output_grid = np.empty((0, 0), dtype=int)

    return output_grid
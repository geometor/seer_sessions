"""
Identify U-shaped patterns and place a yellow marker below the center of each in the last row.

The transformation identifies specific 'U'-shaped objects within the input grid. 
A 'U' shape is defined as a 3-pixel wide, 2-pixel high block where:
- The top row (r) consists of three pixels of the same non-white color (C): C, C, C.
- The bottom row (r+1) consists of the same color C, white (0), and C: C, 0, C.
For each identified 'U' shape starting at row `r` and column `c`, a yellow pixel (color 4) is placed in the output grid. 
This yellow pixel is located in the last row of the grid, specifically at the column index corresponding to the center of the 'U' shape's top row (column `c+1`). 
The rest of the input grid remains unchanged in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Identifies U-shaped patterns in the input grid and adds a yellow marker 
    in the last row below the center of each pattern.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid with markers added.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Create a copy of the input grid to modify
    output_grid = grid.copy()

    # Define the marker color
    marker_color = 4 # yellow

    # Iterate through the grid to find the top-left corner of potential U-shapes
    # We only need to check up to height-2 and width-3 to fit the 3x2 pattern
    for r in range(height - 1):
        for c in range(width - 2):
            # Get the color of the potential top-left pixel
            color_c = grid[r, c]

            # Skip if the potential starting pixel is white (0)
            if color_c == 0:
                continue

            # Check if the 3x2 area matches the U-shape pattern
            # Check top row: C, C, C
            if (grid[r, c+1] == color_c and grid[r, c+2] == color_c):
                # Check bottom row: C, 0, C
                if (grid[r+1, c] == color_c and 
                    grid[r+1, c+1] == 0 and 
                    grid[r+1, c+2] == color_c):
                    
                    # If a U-shape is found, place the marker in the last row
                    # The marker's column is the center of the U-shape's top row (c+1)
                    last_row_index = height - 1
                    center_col_index = c + 1
                    
                    # Place the yellow marker in the output grid
                    output_grid[last_row_index, center_col_index] = marker_color

    # Convert the modified NumPy array back to a list of lists before returning
    return output_grid.tolist()
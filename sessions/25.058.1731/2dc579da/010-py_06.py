"""
1.  **Locate the Target:** Find the single blue (1) pixel within the input grid.
2.  **Define the Region:** Create a 3x3 window centered on the blue pixel. If the blue pixel is on the edge, the window will still be 3x3 and go out of bounds on the input array.
3.  **Extract:** Extract the pixels within this 3x3 window.
4. **Output**: Output is the extracted 3x3 region.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    # Find coordinates of a pixel with the specified color
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return first occurrence
    return None

def transform(input_grid):
    """
    Transforms the input grid by extracting a 3x3 subgrid centered on the blue pixel.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # Locate the target (blue pixel)
    blue_pixel_coords = find_pixel_by_color(input_grid, 1)

    if blue_pixel_coords is None:
        return input_grid # if no blue pixel return the original.

    # Define the region (3x3 window)
    row, col = blue_pixel_coords
    row_start = row - 1
    row_end = row + 2
    col_start = col - 1
    col_end = col + 2

    # Extract the 3x3 region.  Numpy handles out-of-bounds slicing gracefully.
    output_grid = input_grid[row_start:row_end, col_start:col_end]
    
    return output_grid.tolist()
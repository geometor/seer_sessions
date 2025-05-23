"""
The transformation identifies the contiguous region of blue (1) pixels in the input grid, finds the minimum and maximum row and column indices of these blue pixels, and then extracts this subgrid. Finally, it creates an output grid where any pixel that was blue (1) in the input subgrid remains blue (1), and all other pixels are set to white (0).
"""

import numpy as np

def get_bounding_box(grid, color):
    # Find all coordinates of pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Return None if no pixels of the specified color are found

    # Find minimum and maximum row and column indices.
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Identify the bounding box of the blue region (color 1).
    bounding_box = get_bounding_box(input_array, 1)

    if bounding_box is None:
      return []

    (min_row, min_col), (max_row, max_col) = bounding_box

    # Initialize the output grid with white pixels (0).
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Extract subgrid and set blue
    for r in range(output_height):
        for c in range(output_width):
            if input_array[min_row + r, min_col + c] == 1:
                output_grid[r,c] = 1

    return output_grid.tolist()
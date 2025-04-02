"""
Identifies a single contiguous non-white object in the input grid.
Calculates the horizontal distance needed to move the object so its rightmost edge aligns with the rightmost column of the grid.
Creates a new grid of the same dimensions, initially filled with white (0).
Places the object, preserving its shape and color, into the new grid at the calculated shifted horizontal position.
"""

import numpy as np

def find_object_pixels(grid):
    """
    Finds all non-background (non-0) pixels, assumes they form a single object.
    Returns a list of their coordinates (row, col) and the object's color.
    """
    pixels = []
    object_color = None
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                pixels.append((r, c))
                if object_color is None:
                    object_color = grid[r, c]
                elif grid[r, c] != object_color:
                    # This case shouldn't happen based on the problem description,
                    # but good practice to consider. We'll assume the first non-zero color found.
                    pass 
    return pixels, object_color

def transform(input_grid):
    """
    Moves the single non-white object in the grid horizontally to the right edge.
    """
    # Convert input list of lists to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    grid_height, grid_width = input_np.shape
    
    # Initialize output_grid with the background color (0)
    output_grid = np.zeros_like(input_np)

    # 1. Identify all non-white pixels (the object) and its color.
    object_pixels, object_color = find_object_pixels(input_np)

    # If there's no object, return the empty grid
    if not object_pixels:
        return output_grid.tolist() # Convert back to list of lists for output

    # 2. Determine the rightmost column index occupied by the object.
    max_col_obj = -1
    for r, c in object_pixels:
        if c > max_col_obj:
            max_col_obj = c

    # 3. Determine the width of the input grid (already done).
    # grid_width = input_np.shape[1]

    # 4. Calculate the horizontal shift distance.
    shift = (grid_width - 1) - max_col_obj

    # 5. Create the output grid (already done).

    # 6. Iterate through each pixel of the object and place it in the shifted position.
    for r, c in object_pixels:
        # a. Calculate the new column position.
        new_col = c + shift
        # b. Place the pixel in the output grid, checking bounds just in case.
        if 0 <= r < grid_height and 0 <= new_col < grid_width:
             output_grid[r, new_col] = object_color

    # 7. Return the resulting grid as a list of lists.
    return output_grid.tolist()

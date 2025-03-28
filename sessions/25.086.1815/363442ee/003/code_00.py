"""
Transforms an input grid based on the following rules:
1. Create a new output grid with the same dimensions as the input grid, filled with white (0).
2. Copy all gray (5) pixels from the input grid to the corresponding coordinates in the output grid.
3. Extract the 3x3 'source pattern' from the top-left corner (0,0 to 2,2) of the input grid.
4. Copy this 'source pattern' to the top-left corner (0,0 to 2,2) of the output grid, but do not overwrite any gray pixels already placed.
5. Find the coordinates of all blue (1) 'marker' pixels in the input grid.
6. For each marker coordinate, stamp the 'source pattern' onto the output grid, anchored at the marker's coordinate (top-left of pattern aligns with marker).
7. During stamping, ensure coordinates are within grid bounds and do not overwrite any gray (5) pixels in the output grid.
"""

import numpy as np

def find_pixels(grid, color):
    """
    Finds the coordinates of all pixels with a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple is (row, col) coordinate.
    """
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    grid_height, grid_width = input_grid_np.shape
    
    background_color = 0
    preserve_color = 5
    marker_color = 1
    
    # 1. Initialize output grid with background color (white, 0)
    output_grid = np.full((grid_height, grid_width), background_color, dtype=int)

    # 2. Identify and copy 'preserve' color pixels (gray, 5)
    preserve_coords = find_pixels(input_grid_np, preserve_color)
    for r, c in preserve_coords:
        # Check bounds just in case, though coordinates come from the grid itself
        if 0 <= r < grid_height and 0 <= c < grid_width:
            output_grid[r, c] = preserve_color

    # 3. Extract the 3x3 source pattern from the top-left corner
    # Ensure pattern extraction does not go out of bounds for small grids
    pattern_height = min(3, grid_height)
    pattern_width = min(3, grid_width)
    source_pattern = input_grid_np[0:pattern_height, 0:pattern_width]

    # 4. Copy the source pattern to the top-left of the output grid,
    #    avoiding overwriting preserved (gray) pixels.
    for dr in range(pattern_height):
        for dc in range(pattern_width):
             r_out, c_out = dr, dc # Target coordinates are same as relative pattern coords
             # Check if the target pixel is NOT the preserved color before overwriting
             if output_grid[r_out, c_out] != preserve_color:
                 output_grid[r_out, c_out] = source_pattern[dr, dc]

    # 5. Find the coordinates of all marker pixels (blue, 1) in the input grid.
    marker_coords = find_pixels(input_grid_np, marker_color)

    # 6. For each marker coordinate, stamp the source pattern onto the output grid.
    for r_marker, c_marker in marker_coords:
        # a. Iterate through each pixel of the source pattern
        for dr in range(pattern_height):
            for dc in range(pattern_width):
                # b. Calculate the target coordinate in the output grid
                r_out = r_marker + dr
                c_out = c_marker + dc

                # c. Check if the target coordinate is within the boundaries
                if 0 <= r_out < grid_height and 0 <= c_out < grid_width:
                    # d/e. Check if the target pixel is NOT gray before stamping
                    if output_grid[r_out, c_out] != preserve_color:
                        output_grid[r_out, c_out] = source_pattern[dr, dc]

    # 7. Return the final output grid as a list of lists
    return output_grid.tolist()

import numpy as np

"""
1. Initialize an 8x8 output grid filled entirely with orange (7).
2. Identify the single non-orange pixel (the "marker pixel") in the 8x8 input grid. Record its color and its coordinates (row, col).
3. Determine if the marker pixel is in a 'top' corner (row = 0) or a 'bottom' corner (row = 7).
4. Based on the marker pixel's specific corner location and whether it's a 'top' or 'bottom' corner, calculate the coordinates for a set of pixels to be drawn on the output grid using the marker pixel's color:
    - If the marker is at the top-left (0, 0), calculate coordinates relative to the marker: (+1,+1), (+1,+2), (+2,+1), (+2,+2).
    - If the marker is at the top-right (0, 7), calculate coordinates relative to the marker: (+1,-2), (+1,-1), (+2,-2), (+2,-1).
    - If the marker is at the bottom-left (7, 0), calculate coordinates relative to the marker: (-3,+2), (-2,+2), (-1,+3).
    - If the marker is at the bottom-right (7, 7), calculate coordinates relative to the marker: (-3,-2), (-2,-2), (-1,-3).
5. Change the color of the calculated pixels on the output grid to the marker pixel's color.
6. The resulting grid is the final output.
"""

def find_marker_pixel(grid, background_color):
    """
    Finds the coordinates (row, col) and color of the first pixel
    that does not match the background color.
    Assumes exactly one such pixel exists in a corner.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                # Check if it's a corner pixel (although logic later enforces this)
                is_corner = (r == 0 or r == rows - 1) and (c == 0 or c == cols - 1)
                if is_corner:
                    return r, c, grid[r, c]
    # Should not happen based on task constraints
    return None, None, None

def transform(input_grid):
    """
    Transforms the input grid by finding a corner marker pixel and drawing
    a corresponding shape (2x2 square for top corners, specific 3-pixel shape
    for bottom corners) in a new location on an orange background.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    background_color = 7 # orange

    # 1. Initialize output_grid with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # 2. Find the marker pixel and its properties
    marker_row, marker_col, marker_color = find_marker_pixel(input_grid_np, background_color)

    # If no marker found (edge case, shouldn't occur based on examples)
    if marker_row is None:
        return output_grid.tolist()

    # 4. Determine the corner and calculate relative coordinates for the output shape
    pixels_to_draw_relative = []
    if marker_row == 0 and marker_col == 0: # Top-left
        pixels_to_draw_relative = [
            (+1, +1), (+1, +2), (+2, +1), (+2, +2) # 2x2 square
        ]
    elif marker_row == 0 and marker_col == cols - 1: # Top-right
        pixels_to_draw_relative = [
            (+1, -2), (+1, -1), (+2, -2), (+2, -1) # 2x2 square
        ]
    elif marker_row == rows - 1 and marker_col == 0: # Bottom-left
        pixels_to_draw_relative = [
            (-3, +2), (-2, +2), (-1, +3) # 3-pixel shape
        ]
    elif marker_row == rows - 1 and marker_col == cols - 1: # Bottom-right
         pixels_to_draw_relative = [
            (-3, -2), (-2, -2), (-1, -3) # 3-pixel shape
        ]

    # 5. Draw the pixels onto the output grid using absolute coordinates
    for dr, dc in pixels_to_draw_relative:
        r, c = marker_row + dr, marker_col + dc
        # Check bounds to ensure pixels are within the grid
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = marker_color
        # else: # Optional: Log if a pixel goes out of bounds, though not expected here
            # print(f"Warning: Calculated pixel ({r}, {c}) is out of bounds.")


    # 6. Return the final grid as a list of lists
    return output_grid.tolist()
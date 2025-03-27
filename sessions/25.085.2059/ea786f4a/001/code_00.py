"""
1. Identify the coordinates (row `r0`, column `c0`) of the single white pixel (color 0) in the input grid. This is the "anchor pixel".
2. Create an output grid with the same dimensions as the input grid.
3. For each pixel at coordinates (row `r`, column `c`) in the input grid:
    a. Calculate the Manhattan distance `d` between this pixel (`r`, `c`) and the anchor pixel (`r0`, `c0`): `d = abs(r - r0) + abs(c - c0)`.
    b. Check if the distance `d` is even or odd.
    c. If `d` is even, set the color of the corresponding pixel (`r`, `c`) in the output grid to white (0).
    d. If `d` is odd, set the color of the corresponding pixel (`r`, `c`) in the output grid to the original color of the input pixel at (`r`, `c`).
4. Return the completed output grid.
"""

import numpy as np

def find_anchor_pixel(grid):
    """Finds the coordinates of the first pixel with value 0."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0:
                return r, c
    return None # Should not happen based on task description

def calculate_manhattan_distance(r1, c1, r2, c2):
    """Calculates the Manhattan distance between two points."""
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid):
    """
    Applies a transformation based on Manhattan distance from a single white pixel.
    Pixels at an even Manhattan distance become white (0).
    Pixels at an odd Manhattan distance retain their original color.
    """
    # Convert input list of lists to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Identify the anchor pixel (the white pixel)
    anchor_r, anchor_c = find_anchor_pixel(input_grid_np)
    if anchor_r is None: # Handle cases where no white pixel is found (though not expected)
        return input_grid # Or raise an error

    # 2. Create an output grid (initialize as a copy of the input)
    output_grid_np = np.copy(input_grid_np)

    # 3. Iterate through each pixel and apply the transformation rule
    for r in range(rows):
        for c in range(cols):
            # a. Calculate Manhattan distance
            distance = calculate_manhattan_distance(r, c, anchor_r, anchor_c)

            # b. Check if distance is even or odd
            # c. If even, set output pixel to white (0)
            if distance % 2 == 0:
                output_grid_np[r, c] = 0
            # d. If odd, the pixel already has the correct color from the copy

    # 4. Return the completed output grid (convert back to list of lists if necessary)
    return output_grid_np.tolist()

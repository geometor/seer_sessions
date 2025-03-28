import numpy as np

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Find the coordinates of all pixels in the input grid that are red (2). These are the seed pixels.
3. For each seed pixel (r0, c0):
    a. Start a diagonal path sequence moving upwards and rightwards from the seed: current coordinate (r, c) starts at (r0, c0).
    b. While the current coordinate (r, c) is within the grid boundaries (row r >= 0 and column c < grid_width):
        i.   Identify three potential target coordinates relative to the current path coordinate (r, c):
             - Target 1: (r, c)
             - Target 2: (r, c + 1)
             - Target 3: (r - 1, c + 1)
        ii.  For each target coordinate (tr, tc):
             - Check if (tr, tc) is within the grid boundaries.
             - If it is within bounds AND the pixel at (tr, tc) in the *original input grid* is white (0):
                 - Set the pixel at (tr, tc) in the *output grid* to red (2).
        iii. Update the current path coordinate for the next step: (r, c) becomes (r - 1, c + 1).
4. Return the modified output grid.
"""

def is_within_bounds(r, c, height, width):
    """Checks if coordinates (r, c) are within the grid dimensions."""
    return 0 <= r < height and 0 <= c < width

def transform(input_grid):
    """
    Applies the diagonal red pattern generation rule based on initial red pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np)

    # Find the coordinates of all red (2) pixels in the input grid
    seed_pixels_r, seed_pixels_c = np.where(input_np == 2)
    seed_coordinates = list(zip(seed_pixels_r, seed_pixels_c))

    # Process each seed pixel
    for r0, c0 in seed_coordinates:
        # Start the diagonal path
        r, c = r0, c0

        # Continue path generation as long as the current path point is valid
        # The primary path check should be on (r, c) itself, as it's the base for targets
        while is_within_bounds(r, c, height, width):
            # Define the three target coordinates relative to the current path point (r, c)
            targets = [
                (r, c),          # Current path point
                (r, c + 1),      # Point to the right
                (r - 1, c + 1)   # Point diagonally up-right
            ]

            # Check and potentially color each target location
            for tr, tc in targets:
                # Check if the target coordinate is within the grid bounds
                if is_within_bounds(tr, tc, height, width):
                    # Check if the corresponding pixel in the *original input grid* is white (0)
                    if input_np[tr, tc] == 0:
                        # If it's white, change the pixel in the *output grid* to red (2)
                        output_grid[tr, tc] = 2

            # Move to the next point in the diagonal path (up and right)
            r, c = r - 1, c + 1
            # The loop condition (is_within_bounds(r, c, ...)) will handle termination

    return output_grid.tolist()
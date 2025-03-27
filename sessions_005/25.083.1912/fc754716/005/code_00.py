"""
Transforms an input grid by identifying a "seed" pixel (the first non-zero pixel), drawing a frame of the seed's color around the output grid, setting the seed and its neighbors to 0, and filling the inner area with the seed's color.
"""

import numpy as np

def get_seed_pixel(grid):
    # Find the coordinates and value of the first non-zero pixel (seed).
    non_zero_indices = np.nonzero(grid)
    if len(non_zero_indices[0]) > 0:
       x = non_zero_indices[0][0]
       y = non_zero_indices[1][0]
       color = grid[x, y]
       return x, y, color
    return None, None, None

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get the seed pixel information
    seed_x, seed_y, seed_color = get_seed_pixel(input_grid)

    if seed_x is None:  # No seed pixel, return original grid
        return input_grid.tolist()

    # Create the frame with the seed color
    output_grid[0, :] = seed_color          # Top row
    output_grid[-1, :] = seed_color         # Bottom row
    output_grid[:, 0] = seed_color          # Left column
    output_grid[:, -1] = seed_color         # Right column

    # Clear seed pixel and its neighbors
    output_grid[seed_x, seed_y] = 0
    if seed_x > 0:
        output_grid[seed_x - 1, seed_y] = 0  # Above
    if seed_x < rows - 1:
        output_grid[seed_x + 1, seed_y] = 0  # Below
    if seed_y > 0:
        output_grid[seed_x, seed_y - 1] = 0  # Left
    if seed_y < cols - 1:
        output_grid[seed_x, seed_y + 1] = 0  # Right

    # Fill the inner area with the seed color
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if output_grid[i, j] == 0:
                output_grid[i, j] = seed_color

    return output_grid.tolist()
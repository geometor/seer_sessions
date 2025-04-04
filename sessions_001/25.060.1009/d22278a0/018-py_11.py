"""
The transformation identifies non-white "seed" pixels and propagates their color to fill columns to the right, stopping at grid edges or other non-white pixels. Red seeds propagate downwards, and yellow seeds propagate upwards.
"""

import numpy as np

def get_seed_pixels(grid):
    """Finds coordinates and colors of non-white pixels."""
    coords = np.argwhere(grid != 0)
    seed_pixels = []
    for r, c in coords:
        seed_pixels.append((r, c, grid[r, c]))
    return seed_pixels

def fill_column(grid, start_row, col, color, direction):
    """Fills a column with the given color, starting from start_row and moving in the specified direction."""
    rows = grid.shape[0]
    if direction == "down":
        for i in range(start_row, rows):
            if grid[i, col] == 0:
                grid[i, col] = color
            else:
                break  # Stop if a non-white pixel is encountered
    elif direction == "up":
        for i in range(start_row, -1, -1):
            if grid[i, col] == 0:
                grid[i, col] = color
            else:
                break  # Stop if a non-white pixel is encountered
    return grid

def transform(input_grid):
    """
    Transforms the input grid according to the color propagation rule.
    """
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Get seed pixels (non-white pixels).
    seed_pixels = get_seed_pixels(input_grid)

    # Propagate color for each seed pixel.
    for r, c, color in seed_pixels:
        # determine fill direction
        if color == 2:  # Red propagates down
            direction = "down"
        elif color == 4: # Yellow propagates up
             direction = "up"
        else:
            continue # ignore other colors

        # propagate to the right of the seed
        for j in range(c, cols):
            output_grid = fill_column(output_grid, 0, j, color, direction)


    return output_grid
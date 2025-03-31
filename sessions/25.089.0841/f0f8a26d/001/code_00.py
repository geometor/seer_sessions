import numpy as np

"""
The transformation consists of three steps:
1. Rotate the input grid 90 degrees counter-clockwise.
2. Apply downward gravity to the non-background pixels within each column of the rotated grid. The most frequent color is considered the background. Non-background pixels in a column fall to the lowest possible positions in that column, maintaining their original vertical order relative to each other.
3. Rotate the resulting grid 90 degrees clockwise to produce the output grid.
"""

def apply_gravity_down(grid, background_color):
    """
    Applies downward gravity to non-background pixels in each column.
    """
    rows, cols = grid.shape
    output_grid = np.full((rows, cols), background_color, dtype=int)

    for j in range(cols):
        # Extract non-background pixels from the column
        column = grid[:, j]
        non_background_pixels = [p for p in column if p != background_color]

        # Place non-background pixels at the bottom of the output column
        num_non_background = len(non_background_pixels)
        if num_non_background > 0:
            output_grid[rows - num_non_background:, j] = non_background_pixels

    return output_grid

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, assuming it's the background.
    Defaults to 0 (black/white depending on map) if grid is empty or uniform.
    """
    unique, counts = np.unique(grid, return_counts=True)
    if len(counts) == 0:
        return 0 # Default background
    background_color = unique[np.argmax(counts)]
    return background_color

def transform(input_grid):
    """
    Applies a counter-clockwise rotation, downward gravity, and clockwise rotation.
    """
    # Find the background color (most frequent pixel value)
    background_color = find_background_color(input_grid)

    # 1. Rotate the input grid 90 degrees counter-clockwise
    rotated_ccw_grid = np.rot90(input_grid, k=1)

    # 2. Apply downward gravity to non-background pixels
    gravity_applied_grid = apply_gravity_down(rotated_ccw_grid, background_color)

    # 3. Rotate the resulting grid 90 degrees clockwise
    output_grid = np.rot90(gravity_applied_grid, k=-1) # k=-1 for clockwise

    return output_grid
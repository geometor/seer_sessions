import numpy as np

"""
Transforms an input grid based on the following rules:
1. Identify all non-white pixels (color > 0) in the input grid.
2. Create a "modified pattern" grid of the same dimensions as the input.
3. Populate the modified pattern grid:
    a. Non-white pixels from the input are copied directly.
    b. White pixels (color 0) from the input are transformed:
        i. If a white pixel is orthogonally adjacent (shares an edge) to any non-white pixel in the original input grid, it becomes blue (1).
        ii. Otherwise, the white pixel becomes green (3).
4. Create the final output grid, which is 3 times the height and 3 times the width of the input grid.
5. Tile the modified pattern grid 3 times horizontally and 3 times vertically to fill the output grid.
"""

def is_orthogonally_adjacent_to_non_white(grid, r, c):
    """
    Checks if a pixel at (r, c) in the grid is orthogonally adjacent
    to any non-white pixel (color > 0).

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the pixel to check.
        c (int): Column index of the pixel to check.

    Returns:
        bool: True if adjacent to a non-white pixel, False otherwise.
    """
    height, width = grid.shape
    # Define orthogonal neighbor offsets
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    for nr, nc in neighbors:
        # Check if neighbor is within grid bounds
        if 0 <= nr < height and 0 <= nc < width:
            # Check if neighbor is non-white
            if grid[nr, nc] > 0:
                return True
    return False

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Create the modified pattern grid
    modified_pattern = np.zeros_like(input_np)

    # Iterate through each pixel of the input grid to create the modified pattern
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]
            if pixel_color > 0:
                # Copy non-white pixels directly
                modified_pattern[r, c] = pixel_color
            else:
                # Transform white pixels based on adjacency
                if is_orthogonally_adjacent_to_non_white(input_np, r, c):
                    modified_pattern[r, c] = 1 # Blue
                else:
                    modified_pattern[r, c] = 3 # Green

    # Create the output grid with 3x dimensions
    output_height = height * 3
    output_width = width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Tile the modified pattern onto the output grid
    for r_out in range(output_height):
        for c_out in range(output_width):
            # Find corresponding pixel in the modified pattern using modulo
            r_mod = r_out % height
            c_mod = c_out % width
            output_grid[r_out, c_out] = modified_pattern[r_mod, c_mod]

    # Convert back to list of lists for the standard ARC format
    return output_grid.tolist()
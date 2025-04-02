import numpy as np
from collections import deque

"""
Transforms the input grid based on the following rules:
1. Identifies all unique colors present in the input grid, excluding the background color (white, 0) and gray (5). These are 'target colors'.
2. For each target color:
    a. Finds all pixels in the input grid matching that color.
    b. Calculates the top-left corner (minimum row, minimum column) of the bounding box containing *all* pixels of that color collectively.
    c. Draws a single 3x3 square of that target color onto an initially white output grid, starting at the calculated overall top-left corner. If squares for different colors overlap, the behavior for overlaps isn't explicitly defined by the examples but processing colors numerically seems reasonable (higher values overwrite lower).
3. Gray pixels (5) from the input are ignored and effectively removed in the output.
4. The output grid has the same dimensions as the input grid and is initialized to white (0).
"""

def get_color_pixels(grid, color):
    """
    Finds all coordinates (row, col) in the grid matching the specified color.

    Args:
        grid (np.array): The input grid.
        color (int): The color to find.

    Returns:
        list: A list of (row, col) tuples for pixels matching the color.
              Returns an empty list if the color is not found.
    """
    # Use np.where to efficiently find the indices where the grid matches the color
    rows, cols = np.where(grid == color)
    # Combine the row and column indices into a list of (row, col) tuples
    return list(zip(rows, cols))

def get_overall_bounding_box_top_left(pixels):
    """
    Calculates the top-left corner (min_row, min_col) of the bounding box
    encompassing the given list of pixel coordinates. This considers all
    provided pixels together to find the overall minimum row and column.

    Args:
        pixels (list): A list of (row, col) coordinates for ALL pixels of a given color.

    Returns:
        tuple: (min_row, min_col) representing the top-left corner.
               Returns (None, None) if the pixels list is empty.
    """
    if not pixels:
        return None, None
    # Find the minimum row index among all pixel coordinates
    min_row = min(r for r, c in pixels)
    # Find the minimum column index among all pixel coordinates
    min_col = min(c for r, c in pixels)
    return min_row, min_col

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid with the same dimensions, filled with the background color (0)
    output_grid = np.zeros_like(input_np)

    # Find all unique colors present in the input grid
    unique_colors = np.unique(input_np)
    # Sort the unique colors numerically. This ensures a consistent order if squares overlap.
    # Based on example 1, overlaps don't seem intended, but sorting provides determinism.
    unique_colors = sorted(unique_colors)


    # Iterate through each unique color found in the input
    for color in unique_colors:
        # Rule 3: Skip the background color (0)
        if color == 0:
            continue
        # Rule 3: Skip the ignored gray color (5)
        if color == 5:
            continue

        # Rule 2a: Get all pixel coordinates for the current target color
        pixels = get_color_pixels(input_np, color)

        # Proceed only if pixels of this color exist
        if pixels:
            # Rule 2b: Calculate the top-left corner of the SINGLE bounding box for ALL these pixels
            min_row, min_col = get_overall_bounding_box_top_left(pixels)

            # Check if a valid top-left corner was found (i.e., pixels list was not empty)
            if min_row is not None and min_col is not None:
                # Rule 2c: Draw ONE 3x3 square of the current color onto the output grid
                # starting from the calculated overall top-left corner.
                for r_offset in range(3):
                    for c_offset in range(3):
                        # Calculate the target row and column in the output grid
                        r_target = min_row + r_offset
                        c_target = min_col + c_offset
                        # Check if the target coordinates are within the grid boundaries
                        if 0 <= r_target < height and 0 <= c_target < width:
                            # Assign the color to the pixel in the output grid
                            # If squares from different colors overlap, the color processed later (higher value due to sorting) will overwrite previous ones.
                            output_grid[r_target, c_target] = color

    # Convert the resulting NumPy array back to a standard list of lists format
    return output_grid.tolist()
import numpy as np
from collections import Counter
import math

"""
Transforms an input grid into a larger output grid based on the location of the most frequent non-white color in the input.

1.  Determine the dimensions (H, W) of the input grid.
2.  Find the most frequent non-white color ('key color') in the input grid.
3.  Create an output grid of size (3*H) x (3*W), initialized with white (0).
4.  Iterate through each cell (r, c) of the input grid.
5.  If the color at input_grid[r, c] matches the 'key color', copy the entire input grid into the corresponding H x W subgrid block in the output grid, starting at position (r*H, c*W).
6.  Return the resulting output grid.
"""

def get_most_frequent_non_white_color(grid):
    """
    Finds the most frequent non-white color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        int or None: The most frequent non-white color, or None if only white is present.
                     If there's a tie, returns the color with the lower numerical value.
    """
    # Flatten the grid and filter out white pixels (0)
    non_white_pixels = grid[grid != 0].flatten()

    if non_white_pixels.size == 0:
        return None  # No non-white pixels

    # Count frequencies
    color_counts = Counter(non_white_pixels)

    # Find the maximum frequency
    max_freq = 0
    if color_counts:
         max_freq = max(color_counts.values())

    # Find all colors with the maximum frequency
    most_frequent_colors = [color for color, count in color_counts.items() if count == max_freq]

    # If there's a tie, return the color with the smallest numerical value
    if not most_frequent_colors:
        return None # Should not happen if non_white_pixels.size > 0 but added for safety
        
    return min(most_frequent_colors)


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Calculate the dimensions of the output grid
    output_H = H * 3
    output_W = W * 3

    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_H, output_W), dtype=int)

    # Find the 'key color' - the most frequent non-white color
    key_color = get_most_frequent_non_white_color(input_np)

    # If no key color is found (e.g., input is all white), return the blank output grid
    if key_color is None:
        return output_grid.tolist() # Convert back to list of lists if needed

    # Iterate through each cell of the input grid
    for r in range(H):
        for c in range(W):
            # Check if the current input cell color matches the key color
            if input_np[r, c] == key_color:
                # Calculate the top-left corner for placing the input grid copy
                start_row = r * H
                start_col = c * W
                end_row = start_row + H
                end_col = start_col + W

                # Copy the entire input grid into the corresponding block in the output grid
                output_grid[start_row:end_row, start_col:end_col] = input_np

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
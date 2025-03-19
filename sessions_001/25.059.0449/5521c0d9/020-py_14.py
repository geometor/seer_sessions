"""
Identify all blue (1), yellow (4), and red (2) pixels as a single combined object.
Shift the entire combined object upwards by the maximum shift amount required by any
part of the object (blue=4, yellow=2, red=1), while maintaining the relative
positions of the colored pixels within the object and respecting grid boundaries.
"""

import numpy as np

def find_colored_pixels(grid):
    """Finds the coordinates of all blue, yellow, and red pixels."""
    blue_coords = np.argwhere(grid == 1)
    yellow_coords = np.argwhere(grid == 4)
    red_coords = np.argwhere(grid == 2)
    return np.concatenate((blue_coords, yellow_coords, red_coords))

def calculate_max_shift(coords, grid):
    """Calculates the maximum upward shift required based on pixel colors."""
    max_shift = 0
    for r, c in coords:
        color = grid[r, c]
        if color == 1:  # Blue
            shift = 4
        elif color == 4:  # Yellow
            shift = 2
        elif color == 2:  # Red
            shift = 1
        else:
            shift = 0
        max_shift = max(max_shift, shift)
    return max_shift


def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros_like(input_grid)

    # Find all colored pixels (combined object)
    colored_coords = find_colored_pixels(input_grid)

    # If no colored pixels, return empty grid (or the original, depending on requirement - here, empty)
    if len(colored_coords) == 0:
        return output_grid

    # Calculate maximum shift
    max_shift = calculate_max_shift(colored_coords, input_grid)

    # Determine the minimum row after shift to check for boundary
    min_row_after_shift = np.min(colored_coords[:, 0]) - max_shift

    # Adjust shift if going out of bounds
    if min_row_after_shift < 0:
        max_shift += min_row_after_shift # Add the negative value to reduce the shift

    # Shift the entire object
    for r, c in colored_coords:
        new_r = r - max_shift
        output_grid[new_r, c] = input_grid[r, c]

    return output_grid
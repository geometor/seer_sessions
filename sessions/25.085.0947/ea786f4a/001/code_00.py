import numpy as np
from typing import List

"""
Change pixel colors based on their Manhattan distance from a single unique white pixel.

1. Identify the coordinates (r0, c0) of the unique white (0) pixel in the input grid.
2. Identify the background color (bg_color) by finding the color of any pixel that is not white (0).
3. Create a new output grid with the same dimensions as the input grid.
4. Iterate through each pixel (r, c) in the grid.
5. Calculate the Manhattan distance d = |r - r0| + |c - c0|.
6. If d is even, set the output pixel (r, c) to white (0).
7. If d is odd, set the output pixel (r, c) to the background color (bg_color).
8. Return the completed output grid.
"""

def find_unique_pixel(grid: np.ndarray, color: int) -> tuple[int, int]:
    """Finds the coordinates of the unique pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if coords.shape[0] != 1:
        # This case should ideally not happen based on the task description
        # but handle defensively. If multiple or no white pixels, raise error or return a default?
        # For now, assume exactly one exists as per perception.
        raise ValueError(f"Expected exactly one pixel with color {color}, found {coords.shape[0]}")
    return tuple(coords[0])

def get_background_color(grid: np.ndarray, exception_color: int) -> int:
    """Finds the color that is not the exception_color. Assumes grid has at least one other color."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != exception_color:
                return grid[r, c]
    # This case should also not happen if the input grid always has a background.
    # If the grid only contains the exception_color, what should background be?
    # Based on examples, there's always a background color different from white.
    raise ValueError(f"Could not find a background color different from {exception_color}")


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on Manhattan distance parity from the unique white pixel.
    Pixels at even distance become white (0), pixels at odd distance become the background color.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # 1. Identify the coordinates of the unique white pixel (0).
    try:
        r0, c0 = find_unique_pixel(grid_np, 0)
    except ValueError as e:
        # Handle cases where the white pixel assumption is violated (e.g., no white pixel)
        # Depending on requirements, could return input, raise error, etc.
        # For now, let's re-raise as it indicates unexpected input based on examples.
        print(f"Error finding unique white pixel: {e}")
        raise

    # 2. Identify the background color.
    try:
        background_color = get_background_color(grid_np, 0)
    except ValueError as e:
        # Handle cases where no background color is found (e.g., grid is all white)
        print(f"Error finding background color: {e}")
        # If the grid is all white (e.g., 1x1 [[0]]), the rule might imply output is [[0]].
        # Let's handle the 1x1 case specifically.
        if height == 1 and width == 1 and grid_np[0,0] == 0:
             return [[0]] # Output for a single white pixel is just that pixel.
        raise # Re-raise for other unexpected cases

    # 3. Create a new output grid, initialized (e.g., with zeros).
    output_grid = np.zeros_like(grid_np)

    # 4. Iterate through each pixel in the grid.
    for r in range(height):
        for c in range(width):
            # 5. Calculate Manhattan distance to the white pixel.
            distance = abs(r - r0) + abs(c - c0)

            # 6. Check if the distance is even or odd.
            if distance % 2 == 0:
                # 7. If even, set output pixel to white (0).
                output_grid[r, c] = 0
            else:
                # 8. If odd, set output pixel to the background color.
                output_grid[r, c] = background_color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()

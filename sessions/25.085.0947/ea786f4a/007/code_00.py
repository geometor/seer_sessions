"""
Transforms the input grid based on the Manhattan distance (d) of each pixel from a unique white (0) pixel present in the input grid.

1. Find the coordinates (r0, c0) of the unique white (0) pixel.
2. Find the background color (bg), which is the non-white color present.
3. Create an output grid of the same size.
4. For each pixel (r, c):
    a. Calculate the Manhattan distance d = |r - r0| + |c - c0|.
    b. Determine the output color based on d and bg:
        i.   If d == 0, the output color is white (0).
        ii.  If d is odd, the output color is the background color (bg).
        iii. If d is even and d > 0:
             1. If bg is Blue (1), the output color is white (0).
             2. If bg is Red (2):
                 - If (d // 2) is odd, the output color is Red (2).
                 - If (d // 2) is even, the output color is white (0).
             3. If bg is Green (3):
                 - If (d // 2) is odd, the output color is white (0).
                 - If (d // 2) is even, the output color is Green (3).
             4. (Default for other bg colors): Assume the output color is white (0).
5. Return the output grid.
"""

import numpy as np
from typing import List, Tuple

def find_unique_pixel(grid: np.ndarray, color: int) -> Tuple[int, int]:
    """Finds the coordinates of the unique pixel with the specified color."""
    # Find all occurrences of the color
    coords = np.argwhere(grid == color)
    # Check if exactly one was found
    if coords.shape[0] != 1:
        raise ValueError(f"Expected exactly one pixel with color {color}, found {coords.shape[0]}")
    # Return as (row, col) tuple
    return tuple(coords[0])

def get_background_color(grid: np.ndarray, exception_color: int) -> int:
    """Finds a color in the grid that is not the exception_color."""
    # Get unique colors present in the grid
    unique_colors = np.unique(grid)
    # Iterate through unique colors to find one that is not the exception
    for color in unique_colors:
        if color != exception_color:
            return color
    # If no other color is found, raise an error
    # This assumes the input grid structure always includes a background color
    raise ValueError(f"Could not find a background color different from {exception_color}")

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies a transformation based on Manhattan distance from a unique white pixel,
    with rules depending on the background color and distance parity.
    """
    # Convert input list of lists to a numpy array for efficient operations
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Handle edge case: Empty grid
    if height == 0 or width == 0:
        return []

    # Handle edge case: 1x1 grid - follows d=0 rule if it's the white pixel
    if height == 1 and width == 1:
        if grid_np[0,0] == 0:
             return [[0]]
        else:
             # According to task rules, input must contain the unique white pixel.
             raise ValueError("Input 1x1 grid does not contain the required white pixel.")

    # 1. Identify the coordinates of the unique white pixel (0).
    try:
        r0, c0 = find_unique_pixel(grid_np, 0)
    except ValueError as e:
        print(f"Error finding unique white pixel: {e}")
        # Re-raise the error to halt execution if the assumption isn't met
        raise

    # 2. Identify the background color.
    try:
        background_color = get_background_color(grid_np, 0)
    except ValueError as e:
        print(f"Error finding background color: {e}")
        # Re-raise the error
        raise

    # 3. Create a new output grid, initialized (e.g., with zeros or empty).
    # Using np.empty is slightly more efficient if all cells will be filled.
    output_grid = np.empty_like(grid_np, dtype=int)

    # 4. Iterate through each pixel in the grid.
    for r in range(height):
        for c in range(width):
            # 4a. Calculate Manhattan distance to the white pixel.
            distance = abs(r - r0) + abs(c - c0)

            # 4b. Determine output color based on distance and background color rules.

            # 4b.i: Rule for d = 0
            if distance == 0:
                output_color = 0 # white
            # 4b.ii: Rule for odd d
            elif distance % 2 != 0:
                output_color = background_color
            # 4b.iii: Rule for even d > 0
            else: # distance is even and > 0
                half_d = distance // 2
                
                # Default output for even distance is white (covers bg=1 and others)
                output_color = 0 

                # Special rule for Red background (bg=2)
                if background_color == 2:
                    if half_d % 2 != 0: # half_d is odd
                        output_color = 2 # Red
                # Special rule for Green background (bg=3)
                elif background_color == 3:
                    if half_d % 2 == 0: # half_d is even
                        output_color = 3 # Green

            # Assign the calculated color to the output grid
            output_grid[r, c] = output_color

    # 5. Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
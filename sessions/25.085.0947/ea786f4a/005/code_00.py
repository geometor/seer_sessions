import numpy as np
from typing import List, Tuple

"""
Transforms the input grid based on Manhattan distance from a unique white pixel, with a special conditional rule for even distances when the background color is Green (3).

1. Find the coordinates (r0, c0) of the unique white (0) pixel.
2. Find the background color (bg), which is the non-white color present.
3. Create an output grid of the same size.
4. For each pixel (r, c):
    a. Calculate the Manhattan distance d = |r - r0| + |c - c0|.
    b. Determine the output color based on d and bg:
        i.   If d == 0, the output color is white (0).
        ii.  If d is odd, the output color is the background color (bg).
        iii. If d is even and d > 0:
             1. If bg is Green (3):
                 - If (d // 2) is odd, the output color is Green (3).
                 - If (d // 2) is even, the output color is white (0).
             2. If bg is not Green (3):
                 - The output color is white (0).
5. Return the output grid.
"""

def find_unique_pixel(grid: np.ndarray, color: int) -> Tuple[int, int]:
    """Finds the coordinates of the unique pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if coords.shape[0] != 1:
        raise ValueError(f"Expected exactly one pixel with color {color}, found {coords.shape[0]}")
    # Return as (row, col) tuple
    return tuple(coords[0])

def get_background_color(grid: np.ndarray, exception_color: int) -> int:
    """Finds a color in the grid that is not the exception_color."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != exception_color:
            return color
    # Handle case where only the exception color exists or grid is empty
    raise ValueError(f"Could not find a background color different from {exception_color}")

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies a transformation based on Manhattan distance from a unique white pixel,
    with a special rule for even distances depending on the background color.
    """
    # Convert input list of lists to a numpy array for efficient operations
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Handle edge case: Empty grid
    if height == 0 or width == 0:
        return []
        
    # Handle edge case: 1x1 grid - follows d=0 rule
    if height == 1 and width == 1:
        if grid_np[0,0] == 0:
             return [[0]]
        else:
             # Input violates assumption of unique white pixel if not 0
             raise ValueError("Input 1x1 grid does not contain the required white pixel.")

    # 1. Identify the coordinates of the unique white pixel (0).
    try:
        r0, c0 = find_unique_pixel(grid_np, 0)
    except ValueError as e:
        print(f"Error finding unique white pixel: {e}")
        raise # Propagate error

    # 2. Identify the background color.
    try:
        background_color = get_background_color(grid_np, 0)
    except ValueError as e:
        print(f"Error finding background color: {e}")
        raise # Propagate error

    # 3. Create a new output grid, initialized (e.g., with zeros).
    output_grid = np.zeros_like(grid_np)

    # 4. Iterate through each pixel in the grid.
    for r in range(height):
        for c in range(width):
            # 4a. Calculate Manhattan distance to the white pixel.
            distance = abs(r - r0) + abs(c - c0)

            # 4b. Determine output color based on distance and background color rules.
            output_color = -1 # Initialize with invalid value

            # 4b.i: Rule for d = 0
            if distance == 0:
                output_color = 0
            # 4b.ii: Rule for odd d
            elif distance % 2 != 0:
                output_color = background_color
            # 4b.iii: Rule for even d > 0
            else: # distance is even and > 0
                # 4b.iii.1: Check if background is Green (3)
                if background_color == 3:
                    half_d = distance // 2
                    # 4b.iii.1.a/b: Rule based on parity of half_d
                    if half_d % 2 != 0: # half_d is odd
                        output_color = background_color # Green (3)
                    else: # half_d is even
                        output_color = 0 # white
                # 4b.iii.2: Rule if background is NOT Green (3)
                else:
                    output_color = 0 # white

            # Assign the calculated color to the output grid
            output_grid[r, c] = output_color

    # 5. Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
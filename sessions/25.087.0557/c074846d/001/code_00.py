import numpy as np
from typing import List, Tuple

"""
Transforms the input grid by performing a 90-degree clockwise rotation of red (2) pixels around a gray (5) pivot pixel.
The original red pixels are changed to green (3) in place, and the rotated positions are marked with red (2).

1. Initialize the output grid as a copy of the input grid.
2. Find the coordinates (gr, gc) of the single gray (5) pixel (pivot).
3. Find the coordinates of all red (2) pixels.
4. For each red pixel (r, c):
   a. Change the pixel at (r, c) in the output grid to green (3).
   b. Calculate the relative position to the pivot: dx = r - gr, dy = c - gc.
   c. Rotate the relative position 90 degrees clockwise: new_dx = dy, new_dy = -dx.
   d. Calculate the new absolute position: new_r = gr + new_dx, new_c = gc + new_dy.
   e. If (new_r, new_c) is within the grid bounds, change the pixel at (new_r, new_c) in the output grid to red (2).
5. Return the modified output grid.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all pixels of a specific color in the grid."""
    coords = np.argwhere(grid == color)
    # Convert numpy array coordinates to list of tuples (row, col)
    return [tuple(coord) for coord in coords]

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the rotation and color change transformation.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    height, width = grid_np.shape

    # Find the gray pivot pixel (color 5)
    # Assumes exactly one gray pixel exists based on examples
    pivot_coords_list = find_pixels(grid_np, 5)
    if not pivot_coords_list:
        # Handle cases where the pivot might be missing, though not seen in examples
        return input_grid # Or raise an error
    gr, gc = pivot_coords_list[0]

    # Find all red pixels (color 2)
    red_pixel_coords = find_pixels(grid_np, 2)

    # Process each red pixel
    for r, c in red_pixel_coords:
        # Change original red pixel to green in the output grid
        output_grid[r, c] = 3

        # Calculate relative position to pivot
        dx = r - gr
        dy = c - gc

        # Rotate 90 degrees clockwise
        new_dx = dy
        new_dy = -dx

        # Calculate new absolute position
        new_r = gr + new_dx
        new_c = gc + new_dy

        # Check if the new position is within grid bounds
        if 0 <= new_r < height and 0 <= new_c < width:
            # Place a new red pixel at the rotated position in the output grid
            output_grid[new_r, new_c] = 2

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
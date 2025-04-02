```python
"""
Identify non-white pixels in the input grid. For each non-white pixel, examine its 8 neighbors (horizontal, vertical, and diagonal). If none of the neighbors have the same color as the pixel itself, change that pixel to white (0) in the output grid. Otherwise, keep the pixel's original color. White (0) pixels remain white.
"""

import numpy as np

# Define relative coordinates for the 8 neighbors
NEIGHBOR_OFFSETS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1), (1, 0), (1, 1)
]

def _has_same_color_neighbor(grid, r, c):
    """
    Helper function to check if the pixel at (r, c) in the grid has any neighbor
    (out of the 8 surrounding cells) with the same color.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.

    Returns:
        bool: True if at least one neighbor has the same color, False otherwise.
    """
    rows, cols = grid.shape
    pixel_color = grid[r, c]

    # Iterate through all 8 neighbor positions
    for dr, dc in NEIGHBOR_OFFSETS:
        nr, nc = r + dr, c + dc
        # Check if the neighbor coordinates are within the grid boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check if the neighbor pixel has the same color
            if grid[nr, nc] == pixel_color:
                return True # Found a neighbor with the same color

    # If the loop completes without finding a same-colored neighbor
    return False

def transform(input_grid_list):
    """
    Transforms the input grid by removing non-white pixels that are isolated.
    A pixel is considered isolated if none of its 8 neighbors (including diagonals)
    have the same color. White pixels remain unchanged.

    Args:
        input_grid_list (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape
    
    # Initialize the output grid as a copy of the input grid
    # This ensures that pixels that don't need changing retain their original color
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for r in range(rows):
        for c in range(cols):
            # We only need to evaluate non-white pixels
            if input_grid[r, c] != 0:
                # Use the helper function to check if the pixel has any neighbors
                # with the same color.
                if not _has_same_color_neighbor(input_grid, r, c):
                    # If the pixel has NO neighbors of the same color, it's considered isolated.
                    # Change this pixel's color to white (0) in the output grid.
                    output_grid[r, c] = 0
            # Else (if pixel is white OR if it's non-white but has same-colored neighbors):
            # No action is needed because the output_grid was initialized as a copy.

    # Convert the final numpy array back to a list of lists format for the ARC standard
    return output_grid.tolist()
```
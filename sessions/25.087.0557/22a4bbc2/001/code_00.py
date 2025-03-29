"""
Processes an input grid based on adjacency rules between blue (1) and azure (8) pixels.

1. Creates an output grid initialized as a copy of the input grid.
2. Iterates through each pixel of the input grid.
3. For each pixel:
   - If the pixel is blue (1), checks its 8 neighbors (horizontal, vertical, diagonal).
     If any neighbor is azure (8), the corresponding pixel in the output grid is set to red (2).
   - If the pixel is azure (8), checks its 8 neighbors.
     If any neighbor is blue (1), the corresponding pixel in the output grid is set to red (2).
   - Otherwise (if the pixel is not blue (1) or azure (8), or if the conditions above are not met),
     the pixel in the output grid retains its original color from the input grid copy.
4. Returns the modified output grid.
"""

import numpy as np

def _has_neighbor_color(grid, r, c, target_color):
    """
    Checks if any of the 8 neighbors of cell (r, c) in the grid has the target_color.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        target_color (int): The color to look for in neighbors.

    Returns:
        bool: True if a neighbor with target_color is found, False otherwise.
    """
    height, width = grid.shape
    # Iterate through all 8 neighbor offsets (dr, dc)
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            # Check if the neighbor coordinates are within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor has the target color
                if grid[nr, nc] == target_color:
                    return True
    # No neighbor with the target color found
    return False

def transform(input_grid):
    """
    Transforms the input grid based on blue (1) and azure (8) adjacency.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Initialize the output grid as a copy of the input grid
    # This handles cases where pixels don't change color
    output_grid = grid_np.copy()

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            current_color = grid_np[r, c]

            # Check if the current pixel is blue (1)
            if current_color == 1:
                # Check if any neighbor is azure (8)
                if _has_neighbor_color(grid_np, r, c, 8):
                    # If yes, change the corresponding output pixel to red (2)
                    output_grid[r, c] = 2
            # Check if the current pixel is azure (8)
            elif current_color == 8:
                # Check if any neighbor is blue (1)
                if _has_neighbor_color(grid_np, r, c, 1):
                    # If yes, change the corresponding output pixel to red (2)
                    output_grid[r, c] = 2
            # No action needed for other colors, as the output grid was initialized as a copy

    # Convert the final NumPy array back to a list of lists before returning
    return output_grid.tolist()

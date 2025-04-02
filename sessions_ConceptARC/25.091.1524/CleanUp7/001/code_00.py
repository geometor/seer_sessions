"""
Identify and remove azure (8) pixels and any non-white pixels adjacent (including diagonals) to them, replacing them with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing azure pixels (8) and any non-white, 
    non-azure pixels adjacent (8-connectivity) to them, replacing them with white (0).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to NumPy array for easier handling
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Set to store coordinates of azure pixels
    azure_coords = set()
    # Set to store coordinates of non-white, non-azure pixels adjacent to azure pixels
    adjacent_coords = set()

    # --- Step 1: Identify all azure pixels ---
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 8:
                azure_coords.add((r, c))

    # --- Step 2: Identify non-white, non-azure pixels adjacent to azure pixels ---
    # Define 8-connectivity neighbors (including diagonals)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for r in range(height):
        for c in range(width):
            pixel_color = grid[r, c]
            # Check if the pixel is non-white (0) and non-azure (8)
            if pixel_color != 0 and pixel_color != 8:
                is_adjacent_to_azure = False
                # Check all 8 neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is an azure pixel
                        if (nr, nc) in azure_coords:
                            is_adjacent_to_azure = True
                            break # Found an azure neighbor, no need to check others
                
                # If adjacent to an azure pixel, mark this pixel for removal
                if is_adjacent_to_azure:
                    adjacent_coords.add((r, c))

    # --- Step 3: Combine coordinates and modify the output grid ---
    pixels_to_remove = azure_coords.union(adjacent_coords)

    for r, c in pixels_to_remove:
        output_grid[r, c] = 0 # Set to white

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()